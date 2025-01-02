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
import re as _re
#
#	Internals
#
from .. import _settings_console as _settings
from ..ColorAndText import cat as _cat
from .styles import _ThemeColors, _ThemeStyle, _ListStyle, _ListColor, _ThemeProperty, _ThemesList
#from . import colors
################################################################################################################
#####                                            Theme Structure                                           #####
################################################################################################################
REQUIRED_ATTRIBUTES = [
	'border_left', 'border_right', 'prompt_read', 'prompt_select', 'bar_empty',
	'bar_half', 'bar_full', 'title_left', 'title_right', 'title_filler',
	'title_bold', 'title_underline', 'title_italic', 'header_left', 'header_right',
	'header_filler', 'bInversedStatus', 'color_fg', 'color_bg', 'status_separators'
]
class Theme:
	"""Trying out, this class instead of named tuple??"""
	def __init__(self, **entries: dict):
		self.__dict__.update(entries)

def sanitize_key(key):
	""" Sanitize a string to be a valid Python identifier """
	key = _re.sub(r'\W|^(?=\d)', '_', key)
	return key



#################################################################################################################
#####                                           Theme Stuff                                                 #####
#################################################################################################################
def list() -> list:
	"""
	Returns a list of themes
	"""
	return {theme for theme in _ThemesList.__members__}

def list_color() -> list:
	"""
	Returns a list of color sets
	"""
	return {color for color in _ListColor.__members__}

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
		# More precice handling below
		pass
	
	if newTheme in _ThemesList.__members__:
		_settings["theme"] = newTheme
		return True
	elif newTheme.lower() == "random":
		import random
		lst_theme = list()
		rnd_theme = random.choice(lst_theme)
		print("\nSaving random:", rnd_theme, "\n")
		_settings[rnd_theme]
	else:
		return False

def get():
	"""
	Retrieves current theme from _settings["theme"] and returns an iterable theme
	"""
	#
	# Get theme values
	#
	theme_name = str(_settings["theme"])
	
	if False:
		# Debug output:
		print("DEBUG - settings:		", _settings)
		print("DEBUG - Themes/& -styles:	", list() ) #_ThemesList.__members__)
		print("DEBUG - Colors:			", list_color() )
		#print("DEBUG - Theme Property:", ) #_ThemeProperty.color , _ThemeProperty.style)
		print()

	# Default handling
	if theme_name in _ThemesList.__members__:
		# Passed theme exists
		theme_raw = _ThemesList[theme_name].value
	elif "custom" == theme_name.lower():
		# Custom theme handling
		_settings["theme"] = theme_name
		this_color = str(_settings["theme_color"])
		this_style = str(_settings["theme_style"])

		#print("DEUBG: custom:: ", this_color, this_style )
		
		# Verify values exist
		if not this_color in _ListColor.__members__ or not this_style in _ListStyle.__members__:
			# Style or Color was not found
			print(f"Theme '{theme_name}' selected, but either color ({this_color}) or style ({this_style}) is invalid or empty.")
			theme_raw = _ThemesList["Default"].value
		else:
			# Generate data
			# Use "enum overkill" to ensure the handling remains identical within the rest of the code
			# This is so I can assign/access the properties of this custom theme the very same way as all other themes
			class _ThisCustom(_Enum):
				CustomTheme = _ThemeProperty(
					color = _ListColor[this_color],
					style = _ListStyle[this_style].value
				)
			# Assign custom enum theme to same var like the other themes
			theme_raw = _ThisCustom.CustomTheme.value
	elif "random" == theme_name.lower():
		print("Random Theme not supported (yet??)")
	else:
		# Provided theme name is not handled
		print(f"The theme name used '{theme_name}' is not supported." , f"\nFalling back to default theme!")
		theme_raw = _ThemesList["Default"].value
	
	#
	# Apply console codes to color attribbutes
	# This applies for for provided themes and custom combinations
	#
	theme_use = {}
	# Extract color attributes
	for attribute, value in theme_raw.color.value.__dict__.items():
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
	
	 # Ensure all required attributes are included with default values
	for attr in REQUIRED_ATTRIBUTES: #theme_raw.__dict__.items(): #REQUIRED_ATTRIBUTES:
		if attr not in theme_use:
			theme_use[attr] = "" if 'color_' not in attr else None
			
	# Return
	Theme = _namedtuple( theme_name, theme_use.keys())
	return Theme(**theme_use)
