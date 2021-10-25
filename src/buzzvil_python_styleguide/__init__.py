# mypy: allow_untyped_calls

import sys

if sys.version_info < (3, 8):
    from typing_extensions import Final
    from importlib_metadata import version
else:
    from typing import Final
    from importlib.metadata import version

__version__: Final[str] = version(__name__)

from buzzvil_python_styleguide.plugin import RequestsTimeoutPlugin  # noqa: E402
