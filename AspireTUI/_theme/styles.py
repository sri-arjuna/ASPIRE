"""
Proves the dataclasses for theme based, styles, colors and properties
"""
################################################################################################################
#####                                            Imports                                                   #####
################################################################################################################
#
#	Prepare data structures
#
#from collections import namedtuple as _namedtuple
from dataclasses import dataclass as _dataclass
from enum import Enum as _Enum

################################################################################################################
#####                                            Style Structure                                           #####
################################################################################################################
#
#	Colors
#
@_dataclass
class _ThemeColors:
	fg: str
	bg: str

class _ListColor(_Enum):
	white_black = _ThemeColors(			fg="white",	bg="black")
	white_blue = _ThemeColors(			fg="white",	bg="blue")
	white_light_blue = _ThemeColors(	fg="white",	bg="light_blue")
	white_dark_gray = _ThemeColors(		fg="white",	bg="dark_gray")
	white_green = _ThemeColors(			fg="white",	bg="green")
	white_red = _ThemeColors(			fg="white",	bg="red")
	light_gray_dark_gray = _ThemeColors(fg="light_gray",	bg="dark_gray")
	black_blue = _ThemeColors(			fg="black",	bg="blue")
	black_light_blue = _ThemeColors(	fg="black",	bg="light_blue")
	black_light_gray = _ThemeColors(	fg="black",	bg="light_gray")
	black_white = _ThemeColors(			fg="black",	bg="white")
	black_cyan = _ThemeColors(			fg="black",	bg="cyan")
	black_light_green = _ThemeColors(	fg="black",	bg="light_green")
	black_light_yellow = _ThemeColors(	fg="black",	bg="light_yellow")

#
#	Styles
#
@_dataclass
class _ThemeStyle:
	border_left: str
	border_right: str
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

class _ListStyle(_Enum):
	Default = _ThemeStyle(
		border_left=" ║ ",		border_right=" ║ ",
		prompt_read="\076\076",	prompt_select="\076\076",
		bar_empty=" ",			bar_half="─",			bar_full="═",
		title_left=" ╟─",		title_right="─╢ ",		title_filler="─",
		title_bold=True,		title_underline=False,	title_italic=True,
		header_left=" ╔═",		header_right="═╗ ",		header_filler="═"
	)
	Classic = _ThemeStyle(
		border_left="# |",		border_right="| #",
		prompt_read="\076",		prompt_select="\076",
		bar_empty=" ",			bar_half="_",			bar_full="=",
		title_left="# |",		title_right="| #",		title_filler=" ",
		title_bold=True,		title_underline=False,	title_italic=False,
		header_left="# |",		header_right="| #",		header_filler=" "
	)
	Console = _ThemeStyle(
		border_left="",			border_right="",
		prompt_read="\076",		prompt_select="\076",
		bar_empty=" ",			bar_half="_",			bar_full="=",
		title_left="",			title_right="",			title_filler=" ",
		title_bold=False,		title_underline=True,	title_italic=False,
		header_left="",			header_right="",		header_filler=" "
	)
	# Blocks = https://en.wikipedia.org/wiki/Block_Elements
	Blocks = _ThemeStyle(
		border_left=" █ ",		border_right=" █ ",
		prompt_read="\076",		prompt_select="\076",
		bar_empty="░",			bar_half="▒",			bar_full="▓",
		title_left=" █▄",		title_right="▄█ ",		title_filler="▀",
		title_bold=True,		title_underline=False,	title_italic=False,
		header_left=" █▀",		header_right="▀█ ",		header_filler="▀"
	)
	Elegance = _ThemeStyle(
		border_left=" █ ",		border_right=" █ ",
		prompt_read="\076",		prompt_select="\076",
		bar_empty="░",			bar_half="▒",			bar_full="▓",
		title_left=" ▄▄",		title_right="▄▄ ",		title_filler="▀",
		title_bold=True,		title_underline=True,	title_italic=True,
		header_left="   ",		header_right="   ",		header_filler=" "
	)
