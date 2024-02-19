import threading
import signal

from junkpy import JunkTypeProcessor

from .containers import MainContainer

from .configuration.configuration_dataclasses import ScrapyardConfig

from .configuration.configuration_parser import ConfigurationParser



class Scrapyard:
	def __init__(self, config_file: str, type_processors: list[JunkTypeProcessor] = None):
		parser = ConfigurationParser(type_processors)
		self._configuration: ScrapyardConfig = parser.load_file(config_file)
		self._running_event = threading.Event()
		self._running = False


	def __stop_signal(self, signum, frame):
		self.stop()


	def run_blocking(self):

		signal.signal(signal.SIGINT, self.__stop_signal)
		signal.signal(signal.SIGTERM, self.__stop_signal)
		
		self._running_event.clear()
		try:
			self.run()
			self._running_event.wait()

		except KeyboardInterrupt:
			self.stop()

		finally:
			if self._running:
				self.stop()
				

	def run(self):
		if self._running:
			raise Exception(f"'{self.__class__.__qualname__}' is already running.")
		
		self._main_container = MainContainer(self._configuration.containers_config)
		self._running = True


	def stop(self):
		if not self._running:
			raise Exception(f"'{self.__class__.__qualname__}' is stopped.")
		
		self._main_container.destroy()
		self._running_event.set()
		self._running = False










	



		
