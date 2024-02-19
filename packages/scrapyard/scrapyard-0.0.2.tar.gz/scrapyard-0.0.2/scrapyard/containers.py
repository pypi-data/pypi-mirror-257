from __future__ import annotations
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
	from .configuration.configuration_dataclasses import ShardConfig
	from .configuration.configuration_dataclasses import ContainerConfig


from .decorators import DependsOn, DependsOnIfExists, DependsOnTags, EventListener, TaggedWith
from .injectors import Injected, InjectedByTags
from .shards import Shard
from concurrent.futures import Future, ThreadPoolExecutor
import importlib
import toposort
import threading



class MainContainer:
	def __init__(self, containers_config: list[ContainerConfig], objects: dict[Any] = None):
		self._objects: dict[Any] = objects if objects is not None else {} 
		self._containers: dict[str, Container] = {}

		for container_config in containers_config:
			container = Container(
				self,
				container_config.name,
				container_config.shards_config,
				container_config.event_pool_workers,
				container_config.objects
			)
			self._containers[container.name] = container


	def send_event(self, destination_container: str, event_name: str, *args, **kwargs) -> Future :
		destination: Container = self._containers[destination_container]
		return destination.send_event(event_name, *args, **kwargs)


	def instance_of(self, container_name: str) -> Container:
		return self._containers[container_name]


	def destroy(self):
		for container in self._containers.values():
			container.destroy()

	@property
	def objects(self):
		return self._objects
			



class Container:
	def __init__(
			self, 
			main_container: MainContainer,
			name: str, 
			shards_config: list[ShardConfig],
			event_pool_workers: int = None,
			objects: dict[Any] = None
		):

		
		self._initialization_lock = threading.Event()
		self._main_container = main_container
		self._name = name
		self._shards: dict[str, Shard] = {}
		self._shards_by_tag: dict[str, set[Shard]] = {}
		self._shards_dependencies: dict[str, set[str]] = {}
		self._event_listeners: dict[str, tuple[Shard, callable]] = {}
		self._event_pool = ThreadPoolExecutor(
			max_workers = event_pool_workers,
			thread_name_prefix = self._name + "EventPool"
		)
		self._objects: dict[Any] = objects if objects is not None else {} 


		for shard_config in shards_config:
			if shard_config.name in self._shards:
				raise Exception(f"Duplicated Shard name '{shard_config.name}'")


			match shard_config.cls.rsplit(".", 1):
				case [module, cls_name]:
					shard_module = importlib.import_module(module) 
					shard_cls = getattr(shard_module, cls_name)

					if not issubclass(shard_cls, Shard):
						raise TypeError(f"Not a subclass of {Shard.__qualname__}: '{shard_config.cls}'")

					shard_instance = shard_cls(shard_config, self)
					shard_instance.__init_shard__(*shard_config.args, **shard_config.kwargs)

					self._shards[shard_config.name] = shard_instance
					for tag in shard_config.tags:
						tag_storage = self._shards_by_tag.get(tag, set())
						tag_storage.add(shard_instance)
						self._shards_by_tag[tag] = tag_storage

					self._shards_dependencies[shard_config.name] = set()

				case _:
					raise ValueError(f"Invalid path for class: '{shard_config.cls}'")


		self.__resolve_shard_metadata__()

		for shard_name in toposort.toposort_flatten(self._shards_dependencies, sort=True):
			self._shards[shard_name].__post_init_shard__()

		self._initialization_lock.set()


	def __resolve_shard_metadata__(self):
		# Tag resolution
		for shard in self._shards.values():
			# Class metadata
			for metadata in getattr(shard.__class__, "_metadata", []):
				match metadata:
					case TaggedWith():
						for tag in metadata.tags:
							tag_storage = self._shards_by_tag.get(tag, set())
							tag_storage.add(shard)
							self._shards_by_tag[tag] = tag_storage


		# Dependency resolution
		for shard in self._shards.values():
			# Class metadata
			for metadata in getattr(shard.__class__, "_metadata", []):
				match metadata:
					case DependsOn() | DependsOnIfExists():
						shard_dependencies: set[str] = self._shards_dependencies.get(shard.name, set())
						for dependency in metadata.dependencies.difference(shard_dependencies):
							if dependency == shard.name:
								continue

							if dependency not in self._shards:
								if metadata.FORCED_DEPENDENCY:
									raise Exception(f"Unknown dependency '{dependency}' for '{shard.name}'.")
							
							else:
								shard_dependencies.add(dependency)

						self._shards_dependencies[shard.name] = shard_dependencies


					case DependsOnTags():
						shard_dependencies: set[str] = self._shards_dependencies.get(shard.name, set())
						for tag in metadata.tags:
							for dependency in self._shards_by_tag.get(tag, set()):
								if dependency != shard.name:
									shard_dependencies.add(dependency.name)

						self._shards_dependencies[shard.name] = shard_dependencies


			# Attributes
			for obj, is_instance_attribute in [
				(shard.__class__, False),
				(shard, True)
			]:
				for attribute_name, attribute_value in vars(obj).items():
					match attribute_value:
						case Injected():
							if is_instance_attribute:
								setattr(obj, attribute_name, self.instance_of(attribute_value.shard_name))
							
							else:
								raise Exception(f"Cannot inject to class attribute '{attribute_name}' on '{shard.name}'.")
							
						case InjectedByTags():
							if is_instance_attribute:
								setattr(obj, attribute_name, self.instances_by_tags_of(*attribute_value.tags))
							
							else:
								raise Exception(f"Cannot inject by tags to class attribute '{attribute_name}' on '{shard.name}'.")
							

						case class_method if callable(class_method):
							for function_metadata in getattr(class_method, "_metadata", []):
								match function_metadata:
									case EventListener():
										if function_metadata.event_name in self._event_listeners:
											raise Exception(f"Duplicated {function_metadata.__class__.__qualname__} '{function_metadata.event_name}'")
										
										self._event_listeners[function_metadata.event_name] = (shard, class_method)



	def instance_of(self, shard_name) -> Shard:
		return self._shards[shard_name]
	
	
	def instances_by_tags_of(self, *tags: str) -> set[Shard]:
		instances = set()
		for tag in frozenset(tags):
			instances_by_tag = self._shards_by_tag.get(tag, None)
			if instances_by_tag:
				instances.update(instances_by_tag)

		return instances



	def send_event(self, event_name: str, *args, **kwargs) -> Future:
		self._initialization_lock.wait()
		(instance, listener) = self._event_listeners[event_name]
		return self._event_pool.submit(listener, instance, *args, **kwargs)


	def destroy(self):
		for shard in self._shards.values():
			shard.__destroy_shard__()
			

	@property
	def main_container(self):
		return self._main_container
	

	@property
	def name(self):
		return self._name


	@property
	def objects(self):
		return self._objects

