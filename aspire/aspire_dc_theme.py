"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""


from dataclasses import dataclass
from enum import Enum
from .aspire_dc_colors import ColorsAndTextCodes as cat


@dataclass
class ThemeAttributes:
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
	header_left: str
	header_right: str
	filler: str


class ThemesList(Enum):
	Default = ThemeAttributes(
		border_left=" ║ ",
		border_right=" ║ ",
		color_fg="white",
		color_bg="blue",
		prompt_read="\076\076",
		prompt_select="\076\076",
		bar_empty=" ",
		bar_half="─",
		bar_full="═",
		title_left=" ╠═",
		title_right="═╣ ",
		header_left=" ╔═",
		header_right="═╗ ",
		filler="═"
	)
	Fedora = ThemeAttributes(
		border_left="# |",
		border_right="| #",
		color_fg="white",
		color_bg="blue",
		prompt_read="\076",
		prompt_select="\076",
		bar_empty=" ",
		bar_half="_",
		bar_full="=",
		title_left="",
		title_right="",
		header_left="",
		header_right="",
		filler=""
	)
	Float = ThemeAttributes(
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
		header_left="",
		header_right="",
		filler=""
	)
	Mono = ThemeAttributes(
		border_left="| |",
		border_right="| |",
		color_fg="black",
		color_bg="white",
		prompt_read="\076",
		prompt_select="\076",
		bar_empty=" ",
		bar_half="_",
		bar_full="=",
		title_left="",
		title_right="",
		header_left="",
		header_right="",
		filler=""
	)


class Theme:
	available_themes = {
		'Default': ThemesList.Default,
		'Fedora': ThemesList.Fedora,
		'Float': ThemesList.Float,
		'Mono': ThemesList.Mono,
	}
	_default = 	"Default"
	_selected = None

	@staticmethod
	def _check_empty_variables(theme):
		empty_variables = []
		var_skip = ["border_left", "border_right", "filler", ]
		for variable_name, variable_value in theme.__dict__.items():
			if variable_name not in var_skip and variable_value == "":
				empty_variables.append(variable_name)
		return empty_variables

	@staticmethod
	def _get_color_code(foreground=None, background=None):
		fg_code = getattr(cat.fg, foreground) if foreground else ""
		bg_code = getattr(cat.bg, background) if background else ""
		return fg_code, bg_code
	
	@classmethod
	def list(cls):
		return cls.available_themes.keys()

	@classmethod
	def set(cls, new_theme):
		if new_theme in cls.available_themes:
			cls.current_theme = cls.available_themes[new_theme]
		else:
			print(f"Theme '{new_theme}' is not available.")

	@classmethod
	def set_custom(cls, custom):
		cls.current_theme = custom
	
	@classmethod
	def get(cls):
		# Get the right theme:
		if cls._selected:
			current_theme = cls.available_themes[cls._selected]
		else:
			current_theme = cls.available_themes[cls._default]
		# Check for empty variables and fill if required:
		empty_variables = cls._check_empty_variables(current_theme.value)
		variables_to_remove = []
		if empty_variables:
			for ev in empty_variables:
				# Try to fill required variables with "default" values, aka regular border
				if "header_left" == ev:
					current_theme._value_.header_left = current_theme._value_.border_left
					variables_to_remove.append(ev)
				if "header_right" == ev:
					current_theme._value_.header_right = current_theme._value_.border_right
					variables_to_remove.append(ev)
				if "title_left" == ev:
					current_theme._value_.title_left = current_theme._value_.title_left
					variables_to_remove.append(ev)
				if "title_right" == ev:
					current_theme._value_.title_right = current_theme._value_.title_right
					variables_to_remove.append(ev)
		# But we always need to encode color:
		current_theme._value_.color_fg, current_theme._value_.color_bg = cls._get_color_code(current_theme._value_.color_fg, current_theme._value_.color_bg)
		for vrt in variables_to_remove:
			empty_variables.remove(vrt)
		if empty_variables:
			print(f"Warning: The following theme variables are still empty: --> {', '.join(empty_variables)}")
		return current_theme.value