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
		border_right="",
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
		border_right="",
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
	_default = "Default"
	_selected = None

	@staticmethod
	def _check_empty_variables(theme):
		empty_variables = []
		for variable_name, variable_value in theme.__dict__.items():
			if isinstance(variable_value, str) and not variable_value.strip():
				empty_variables.append(variable_name)
		return empty_variables

	@classmethod
	def get_color_code(foreground=None, background=None):
		code = ""
		if foreground:
			code += cat.fg.foreground
		if background:
			code += cat.bg.background
		return code
	
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
		if cls._selected:
			selected_theme = cls.available_themes[cls._selected]
			empty_variables = cls._check_empty_variables(selected_theme.value)
			if empty_variables:
				print(f"Warning: The following theme variables are empty: {', '.join(empty_variables)}")
			return selected_theme.value
		else:
			default_theme = cls.available_themes[cls._default]
			empty_variables = cls._check_empty_variables(default_theme.value)
			if empty_variables:
				print(f"Warning: The following theme variables are empty: {', '.join(empty_variables)}")
			return default_theme.value