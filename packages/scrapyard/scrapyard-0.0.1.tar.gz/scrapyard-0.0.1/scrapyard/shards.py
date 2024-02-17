from __future__ import annotations
from datetime import timedelta
import threading
import time
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from .containers import Container, MainContainer 

from abc import ABC, abstractmethod
from .configuration.configuration_dataclasses import ShardConfig


class Shard(ABC):

	def __init__(self, shard_config: ShardConfig, container: Container):
		self._name: str = shard_config.name
		self._tags: frozenset[str] = frozenset(shard_config.tags)
		self._container: Container = container
		

	@property
	def name(self) -> str:
		return self._name


	@property
	def tags(self) -> frozenset:
		return self._tags


	@property
	def container(self) -> Container:
		return self._container
	

	@property
	def main_container(self) -> MainContainer:
		return self._container.main_container
	
	
	def __init_shard__(self, *args, **kwargs):	
		pass


	def __post_init_shard__(self):
		pass


	def __destroy_shard__(self):
		pass



class Task(Shard):
	def __init__(self, shard_config: ShardConfig, container: Container):
		self._running = False
		self._thread = threading.Thread(target=self.__run_thread__, daemon=True)
		super().__init__(shard_config, container)


	def __post_init_shard__(self):
		self._thread.start()


	@property
	def running(self):
		return self._running


	def __run_thread__(self):
		self._running = True
		try:
			self.__run__()

		finally:
			self._running = False

	@abstractmethod
	def __run__(self):
		pass
	

	def __stop__(self):
		self._running = False


	def __destroy_shard__(self):
		self.__stop__()
		self._thread.join()



class IntervalTask(Task):
	def __init__(self, shard_config: ShardConfig, container: Container):
		self._running_event = threading.Event()

		self._uniform_interval = bool(shard_config.options.pop("uniform", False))

		match shard_config.options.pop("interval"):
			case timedelta() as interval:
				self._interval = interval.total_seconds()

			case _ as other:
				self._interval = float(other)


		match shard_config.options.pop("initial_delay", 0):
			case timedelta() as initial_delay:
				self._initial_delay = initial_delay.total_seconds()

			case _ as other:
				self._initial_delay = float(initial_delay)

		super().__init__(shard_config, container)


	def __pre_run__(self):
		pass
	

	def __wait_time__(self, init_timestamp: float) -> float:
		if(self._uniform_interval):
			return max(init_timestamp + self._interval - time.time(), 0)

		return self._interval


	def __run_thread__(self):
		self._running = True
		self._running_event.clear()

		try:
			self._running_event.wait(self._initial_delay)
			if self._running:
				self.__pre_run__()
				while self._running:
					init_t = time.time()
					self.__run__()
					self._running_event.wait(self.__wait_time__(init_t))

		finally:
			self._running = False


	def __stop__(self):
		self._running = False
		self._running_event.set()

