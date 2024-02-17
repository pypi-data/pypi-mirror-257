class Injected:
	def __init__(self, shard_name: str):
		self.shard_name = shard_name


class InjectedByTags:
	def __init__(self, *tags: str):
		self.tags = frozenset(tags)