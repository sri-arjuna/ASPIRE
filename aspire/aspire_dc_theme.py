"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""


from dataclasses import dataclass
from enum import Enum


@dataclass
class ThemeClass:
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


class ThemeEnum(Enum):
	Default = ThemeClass(
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
	Fedora = ThemeClass(
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
	Float = ThemeClass(
		border_left="",
		border_right="",
		color_fg="blue",
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
	Mono = ThemeClass(
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
	available_themes = ['theme1', 'theme2', 'theme3']
	current_theme = 'theme1'

	@classmethod
	def theme_list(cls):
		return cls.available_themes

	@classmethod
	def theme_get(cls):
		return cls.current_theme

	@classmethod
	def theme_set(cls, new_theme):
		if new_theme in cls.available_themes:
			cls.current_theme = new_theme
		else:
			print(f"Theme '{new_theme}' is not available.")

	@classmethod
	def set_custom_theme(cls, custom_theme):
		cls.current_theme = custom_theme
