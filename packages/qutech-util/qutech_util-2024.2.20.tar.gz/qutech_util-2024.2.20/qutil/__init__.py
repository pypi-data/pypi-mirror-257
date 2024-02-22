import lazy_loader

__version__ = '2024.2.20'

"""Lazy imports as described in https://scientific-python.org/specs/spec-0001"""
__getattr__, __dir__, __all__ = lazy_loader.attach_stub(__name__, __file__)

del lazy_loader
