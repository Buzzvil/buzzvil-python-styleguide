try:
    import importlib_metadata
except ModuleNotFoundError:
    import importlib.metadata as importlib_metadata

__version__ = importlib_metadata.version(__name__)

from buzzvil_python_styleguide.plugin import RequestsTimeoutPlugin  # noqa: F401
