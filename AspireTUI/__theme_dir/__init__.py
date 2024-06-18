"""
Provides a list of available color combos for themes.

Set as:\n
from AspireTUI import _the THEME_COLOR = 
"""
# Imports
from .. import Path as _Path


def list_colors() -> list:
	"""Returns the list of found color combos"""
	return _Path.hasFiles("*md", bDual=True)
