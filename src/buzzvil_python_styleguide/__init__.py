from typing_extensions import Final

try:
    from importlib.metadata import version
except ModuleNotFoundError:
    from importlib_metadata import version

__version__: Final[str] = version(__name__)

from buzzvil_python_styleguide.plugin import RequestsTimeoutPlugin  # noqa: E402
