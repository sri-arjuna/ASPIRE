"""
	Description:\n
					Handles themes, data and references.

	Provides:\n
					style = _settings["theme-data"] ; print(theme.border_left)	\n
					list = themes.list()	\n
					themes.set(NAME)		\n
					
	========================================================

	Created on:		2023 Nov. 09

	Created by:		Simon Arjuna Erat

	License:		MIT

	URL:			https://www.github.com/sri-arjuna/ASPIRE

	Based on my TUI & SWARM for the BASH shell © 2011
"""
#from .themes import set_custom_theme, list_available_themes, get_current_theme, load_custom_theme


#import json
#from pathlib import Path

# Load a custom theme from a file
#custom_theme_path = Path.home() / ".config" / "my_custom_theme.json"
#custom_theme = load_custom_theme(custom_theme_path)

# Set the custom theme
#set_custom_theme(custom_theme)

# Now users can include the custom theme in the available themes list
#themes = list_available_themes()
#print(themes)

# Get the current theme, including the custom theme
#current_theme = get_current_theme()
#print(current_theme)

#def load_custom_theme(file_path):
#    try:
#        with open(file_path, 'r') as file:
#            return json.load(file)
#    except FileNotFoundError:
#        print(f"Custom theme file not found at: {file_path}")
#        return None
#    except json.JSONDecodeError:
#        print(f"Error decoding JSON in custom theme file: {file_path}")
#        return None

#def set_custom_theme(custom_theme):
    # Validate custom theme structure if needed
    # ...
#    _available_themes["Custom"] = custom_theme

################################################################################################################
#####                                            Imports                                                   #####
################################################################################################################
#
#	Prepare data structures
#
#from collections import namedtuple as _namedtuple
from dataclasses import dataclass as _dataclass
from collections import namedtuple as _namedtuple
from enum import Enum as _Enum
#
#	Internals
#
from .. import _settings_console as _settings
from ..ColorAndText import cat as _cat
from .styles import _ThemeColors, _ThemeStyle, _ListStyle, _ListColor
#from . import colors
################################################################################################################
#####                                            Theme Structure                                           #####
################################################################################################################
@_dataclass
class _ThemeProperty:
	style: _ThemeStyle
	color: _ThemeColors
	bInversedStatus: bool
	
@_dataclass
class _ThemeAttributes:
	border_left: str
	border_right: str
	color_fg: str
	color_bg: str
	prompt_read: str
	prompt_select: str
	bar_empty: str
	bar_half: str
	bar_full: str
	title_left: str
	title_right: str
	title_filler: str
	title_bold: bool
	title_underline: bool
	title_italic: bool
	header_left: str
	header_right: str
	header_filler: str
	bInversedStatus: bool

class _ThemesList(_Enum):
	Default = _ThemeProperty(
		style = _ListStyle.Default,
		color = _ListColor.white_blue,
		bInversedStatus=False
	)
	Admin = _ThemeProperty(
		style = _ListStyle.Default,
		color = _ListColor.white_red,
		bInversedStatus=False
	)
	Console = _ThemeProperty(
		style = _ListStyle.Console,
		color = _ListColor.white_black,
		bInversedStatus=True
	)
	Classic = _ThemeProperty(
		style = _ListStyle.Classic,
		color = _ListColor.white_blue,
		bInversedStatus=False
	)
	Blocks = _ThemeProperty(
		style = _ListStyle.Blocks,
		color = _ListColor.white_red,
		bInversedStatus=False
	)
	Elegance = _ThemeProperty(
		style = _ListStyle.Elegance,
		color = _ListColor.white_dark_gray,
		bInversedStatus=False
	)
	CyberPunk = _ThemeProperty(
		style = _ListStyle.Elegance,
		color = _ListColor.black_light_yellow,
		bInversedStatus=False
	)
	Skyrim = _ThemeProperty(
		style = _ListStyle.Elegance.value,
		color = _ListColor.white_green,
		bInversedStatus=False
	)

#################################################################################################################
#####                                           Theme Stuff                                                 #####
#################################################################################################################
def list() -> list:
	"""
	Returns a list of themes
	"""
	return {theme for theme in _ThemesList.__members__}

def set(newTheme: str, theme_style=None, theme_color=None):
	"""
	Saves passed string as _settings["theme"] and returns True
	If newTheme is not found in _ThemesList, nothing happens but return False.
	"""
	msg = f"_theme.set(newTheme={newTheme}, theme_style={theme_style}, theme_color={theme_color}), expecting 1 OR 3 arguments. "
	if theme_color is not None:
		if theme_style is not None:
			# Custom theme is passed
			newTheme = "Custom"
			_settings["theme_style"] = theme_style
			_settings["theme_color"] = theme_color
		else:
			print(msg)
			return False
	else:
		# Default behaviour
		pass
	
	if newTheme in _ThemesList.__members__:
		_settings["theme"] = newTheme
		return True
	else:
		return False

def get():
	"""
	Retrieves current theme from _settings["theme"] and returns an iterable object (not notation)
	"""
	#
	# Get theme values
	#
	if _settings["theme"] == "Custom":
		# Special
		for clr in _ListColor.__members__:
			# get Color
			if clr == _settings["theme_color"]:
				Color = _ListColor[clr].value
				break
		for sty in _ListStyle.__members__:
			# get Style
			if sty ==  _settings["theme_style"]:
				Style = _ListStyle[sty].value
		# Generate data
		CustomList = _ThemesList(
			Custom = _ThemeProperty(
				style = Style,
				color = Color,
				bInversedStatus=False
			)
		)
		theme_raw = CustomList.value
	else:
		# Default handling
		theme_raw = _ThemesList[_settings["theme"]].value
	#
	# Apply console codes to color attribbutes
	#
	theme_use = {}
	# Extract color attributes
	for attribute, value in theme_raw.color.value.__dict__.items():
		#print("DEBUG: in color attributes\n%s" % attribute)
		if attribute.startswith('_'):  # Skip internal attributes
			continue
		if 'fg' in attribute:
			theme_use[f"color_{attribute}"] = getattr(_cat.front, value)
		elif 'bg' in attribute:
			theme_use[f"color_{attribute}"] = getattr(_cat.back, value)
		else:
			theme_use[attribute] = value

	# Extract style attributes
	for attribute, value in theme_raw.style.__dict__.items():
		if attribute.startswith('_'):  # Skip internal attributes
			continue
		theme_use[attribute] = value

	# Extract top-level attributes
	_list_top_level = ["bInversedStatus"]
	for attribute, value in theme_raw.__dict__.items():
		if attribute in _list_top_level:
			theme_use[attribute] = value
	
	# Debug
	#for item in theme_use:
	#	print("----- ITEM", item, theme_use[str(item)])
	#	if "border_left" == item:
	#		print("here")
	#print("\nDEBUG:\n%s\n\n" % theme_use.keys())
		
	# Return
	Theme = _namedtuple( _settings["theme"], theme_use.keys())
	return Theme(**theme_use)
	#print("------------------------------", theme_raw)
	#print(theme_use, "------------------------------")
	return type('ThemeData', (), theme_use).__dict__.items()
	#return type('ThemeData', (), theme_use.__getitem__().values())
	#return type('ThemeData', tuple(_ThemeAttributes), theme_use)
	#return _ThemeProperty(theme_use)

them = get()
them
