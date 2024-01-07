"""
	Description:
					Handles themes, data and references.
	Provides:
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
from collections import namedtuple as _namedtuple
from dataclasses import dataclass as _dataclass
from enum import Enum as _Enum
#
#	Internals
#
from . import settings as _settings
from .ColorAndText import cat
################################################################################################################
#####                                            Theme Structure                                           #####
################################################################################################################
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

class _ThemesList(_Enum):
	Default = _ThemeAttributes(
		border_left=" ║ ",
		border_right=" ║ ",
		color_fg="white",
		color_bg="blue",
		prompt_read="\076\076",
		prompt_select="\076\076",
		bar_empty=" ",
		bar_half="─",
		bar_full="═",
		title_left=" ╟─",
		title_right="─╢ ",
		title_filler="─",
		title_bold=True,
		title_underline=False,
		title_italic=True,
		header_left=" ╔═",
		header_right="═╗ ",
		header_filler="═"
	)
	Classic = _ThemeAttributes(
		border_left="# |",
		border_right="| #",
		color_fg="white",
		color_bg="light_blue",
		prompt_read="\076",
		prompt_select="\076",
		bar_empty=" ",
		bar_half="_",
		bar_full="=",
		title_left="# |",
		title_right="| #",
		title_filler=" ",
		title_bold=True,
		title_underline=False,
		title_italic=False,
		header_left="# |",
		header_right="| #",
		header_filler=" "
	)
	Float = _ThemeAttributes(
		border_left="",
		border_right="",
		color_fg="black",
		color_bg="white",
		prompt_read="\076",
		prompt_select="\076",
		bar_empty=" ",
		bar_half="_",
		bar_full="=",
		title_left="",
		title_right="",
		title_filler=" ",
		title_bold=False,
		title_underline=True,
		title_italic=False,
		header_left="",
		header_right="",
		header_filler=" "
	)
	Mono = _ThemeAttributes(
		border_left="| |",
		border_right="| |",
		color_fg="white",
		color_bg="black",
		prompt_read="\076",
		prompt_select="\076",
		bar_empty=" ",
		bar_half="_",
		bar_full="=",
		title_left="| |",
		title_right="| |",
		title_filler=" ",
		title_bold=True,
		title_underline=False,
		title_italic=False,
		header_left="| |",
		header_right="| |",
		header_filler=" "
	)
	Admin = _ThemeAttributes(
		border_left=" ║ ",
		border_right=" ║ ",
		color_fg="white",
		color_bg="red",
		prompt_read="\076\076",
		prompt_select="\076\076",
		bar_empty=" ",
		bar_half="─",
		bar_full="═",
		title_left=" ╠═",
		title_right="═╣ ",
		title_filler="═",
		title_bold=True,
		title_underline=True,
		title_italic=False,
		header_left=" ╔═",
		header_right="═╗ ",
		header_filler="═"
	)
	CyberPunk = _ThemeAttributes(
		border_left=" ║ ",
		border_right=" ║ ",
		color_fg="light_magenta",
		color_bg="light_cyan",
		prompt_read="\076\076",
		prompt_select="\076\076",
		bar_empty=" ",
		bar_half="─",
		bar_full="═",
		title_left=" ╠═",
		title_right="═╣ ",
		title_filler="═",
		title_bold=False,
		title_underline=False,
		title_italic=False,
		header_left=" ╔═",
		header_right="═╗ ",
		header_filler="═"
	)
	# Blocks = https://en.wikipedia.org/wiki/Block_Elements
	Blocks = _ThemeAttributes(
		border_left=" █ ",
		border_right=" █ ",
		color_fg="white",
		color_bg="light_blue",
		prompt_read="\076",
		prompt_select="\076",
		bar_empty="░",
		bar_half="▒",
		bar_full="▓",
		title_left=" █▄",
		title_right="▄█ ",
		title_filler="▀",
		title_bold=True,
		title_underline=False,
		title_italic=False,
		header_left=" █▀",
		header_right="▀█ ",
		header_filler="▀"
	)
# Internal themes
#_available_themes = {theme.name: theme.value for theme in _ThemesList}
#################################################################################################################
#####                                           Theme Stuff                                                 #####
#################################################################################################################
def list() -> list:
	"""
	Returns a list of themese
	"""
	return {theme for theme in _ThemesList.__members__}

def set(newTheme: str):
	"""
	Saves passed string as _settings["theme"] and returns True
	If newTheme is not found in _ThemesList, nothing happens but return False.
	"""
	if newTheme in _ThemesList.__members__:
		_settings["theme"] = newTheme
		return True
	else:
		return False

def get():
	"""
	Retrieves current theme from _settings["theme"] and returns an iterable object (not notation)
	"""
	# Get theme values
	theme_raw = _ThemesList[_settings["theme"]].value

	# Apply console codes to color attribbutes
	theme_use = {}
	for attribute, value in theme_raw.__dict__.items():
		if attribute.startswith('_'):  # Skip internal attributes
			continue
		if 'color_fg' in attribute:
			theme_use[attribute] = getattr(cat.front, value)
		elif 'color_bg' in attribute:
			theme_use[attribute] = getattr(cat.back, value)
		else:
			theme_use[attribute] = value
	
	return type('ThemeData', (), theme_use)
