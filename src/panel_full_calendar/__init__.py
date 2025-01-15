"""Accessible imports for the panel_full_calendar package."""

import importlib.metadata
import warnings

from .main import Calendar
from .main import CalendarEvent

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError as e:  # pragma: no cover
    warnings.warn(f"Could not determine version of {__name__}\n{e!s}", stacklevel=2)
    __version__ = "unknown"

__all__: list[str] = ["Calendar", "CalendarEvent"]
