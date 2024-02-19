from junkpy import JunkTypeProcessor
import importlib


class CustomObjectTypeProcesor(JunkTypeProcessor):
	CLASS = object
	KEYWORD = "custom-object"

	def load(self, value: object, **kwargs) -> object:

		match value:
			case dict():
				cls = value.get("cls", None)
				if cls is None:
					raise Exception(f"Required 'cls' attribute for '{self.KEYWORD}'")

				obj_args = value.get("args", [])
				obj_kwargs = value.get("kwargs", {})

				match cls.rsplit(".", 1):
					case [module_name, cls_name]:
						module = importlib.import_module(module_name) 
						cls_obj = getattr(module, cls_name)
						return cls_obj(*obj_args, **obj_kwargs)

					case _:
						raise ValueError(f"Invalid path for class: '{cls}'")

			case _:
				raise Exception(f"Expected 'dict' object, got '{type(value).__qualname__}'")