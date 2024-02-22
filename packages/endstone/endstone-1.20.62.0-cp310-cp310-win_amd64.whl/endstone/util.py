__all__ = [
    "ColorFormat"
]

for name in __all__:
    from importlib import import_module

    module = import_module("endstone._internal.endstone_python")
    globals()[f"_{name}"] = module.__dict__[name]
    del module

ColorFormat = globals()["_ColorFormat"]
