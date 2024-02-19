from dataclasses import dataclass, field

from ..configuration_dataclasses import ShardConfig
from junkpy import JunkTypeProcessor


@dataclass
class ShardFactory:
	DEFAULT_FORMATTER = "{name}_{index}"
	data: list[dict]
	kwargs: dict = field(default_factory = dict)
	
	def __post_init__(self):
		self.formatter = self.kwargs.pop("formatter", self.DEFAULT_FORMATTER)


	def next(self, name: str) -> list[ShardConfig]:
		for (index, data) in enumerate(self.data):
			if not isinstance(data, dict):
				raise Exception(f"Invalid data format. Expected 'dict', got '{type(data).__qualname__}'")
			

			shard_name = self.formatter.format(
				name = name,
				index = index
			)

			kwargs = self.kwargs.copy()
			kwargs.update(data)
			yield ShardConfig(name=shard_name, **kwargs)
			


	


class ShardFactoryTypeProcesor(JunkTypeProcessor):
	CLASS = ShardFactory
	KEYWORD = "shard-factory"

	def load(self, value: object, **kwargs) -> object:
		if not isinstance(value, list):
			raise Exception(f"Expected 'list' object, got '{type(value).__qualname__}'")

		return self.CLASS(
			data = value, 
			kwargs = kwargs 	
		)
		

