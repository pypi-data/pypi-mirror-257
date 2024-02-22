from __future__ import annotations

from vsr53._version import __version__, __version_tuple__
from vsr53.vsr53 import VSR53DL, VSR53USB

__all__ = ["VSR53DL", "VSR53USB", "__version__", "__version_tuple__"]
