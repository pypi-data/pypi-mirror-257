from typing import List, Optional, Type
from junkpy import JunkParser, JunkTypeProcessor
from junkpy.base import JunkMetadata

from .type_processors.custom_object import CustomObjectTypeProcesor

from .type_processors.shard_factory import ShardFactory, ShardFactoryTypeProcesor

from .configuration_dataclasses import ScrapyardConfig, ShardConfig, ContainerConfig



class ConfigurationParser(JunkParser):
	PARSER_BUILTIN_TYPE_PROCESSORS = [
		ShardFactoryTypeProcesor,
		CustomObjectTypeProcesor
	]

	def __init__(self, type_processors: List[type[JunkTypeProcessor]] | None = None):
		super().__init__(self.PARSER_BUILTIN_TYPE_PROCESSORS + (type_processors if type_processors is not None else []))
		

	def after_parsing(self, metadata: JunkMetadata, parsed_data: object) -> object:
		if not isinstance(parsed_data, dict):
			raise Exception(f"Invalid data structure. Expected 'dict', got '{type(parsed_data)}'")
		
		# Containers
		containers_config_raw = parsed_data.get("containers", {})
		if not isinstance(containers_config_raw, dict):
			raise Exception(f"Invalid data structure for 'containers'. Expected 'dict', got '{type(containers_config_raw)}'")
		
		containers_config = []
		for container_name, container_data in containers_config_raw.items():

			# Shards
			shards_config_raw = container_data.get("shards", {})
			if not isinstance(shards_config_raw, dict):
				raise Exception(f"Invalid data structure for 'shards' on container '{container_name}'. Expected 'dict', got '{type(shards_config_raw)}'")
			
			shards_config = []
			for shard_name, shard_data in shards_config_raw.items():
				match shard_data:
					case dict():
						shards_config.append( 
							ShardConfig(
								name = shard_name,
								**shard_data
							)
						)

					case ShardFactory():
						for shard_config in shard_data.next(shard_name):
							shards_config.append(shard_config)

			# Objects
			container_objects = container_data.get("objects", {})				


			containers_config.append(
				ContainerConfig(
					name = container_name,
					shards_config = shards_config,
					event_pool_workers =  container_data.get("event_pool_workers"),
					objects = container_objects
				)
			)

		# Main container objects
		main_container_objects = parsed_data.get("objects", {}) 

		return ScrapyardConfig(
			containers_config = containers_config,
			objects = main_container_objects
		)
		


