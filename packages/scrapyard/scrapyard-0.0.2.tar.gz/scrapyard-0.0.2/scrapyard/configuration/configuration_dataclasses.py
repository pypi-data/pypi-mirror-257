from dataclasses import dataclass, field
from typing import Any




@dataclass
class ShardConfig:
	name: str
	cls: str
	tags: list[str] = field(default_factory=list)
	options: dict = field(default_factory=dict)
	args: list = field(default_factory=list)
	kwargs: dict = field(default_factory=dict)



@dataclass
class ContainerConfig:
	name: str
	shards_config: list[ShardConfig] = field(default_factory=list)
	event_pool_workers: int = None,
	objects: dict[Any] = field(default_factory=dict)



@dataclass
class ScrapyardConfig:
	containers_config: list[ContainerConfig] = field(default_factory=list)
	objects: dict[Any] = field(default_factory=dict)