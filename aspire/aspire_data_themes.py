# Basic header:
"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""

# Imports
from dataclasses import dataclass
from enum import Enum


################################################################################################################
#####                                              Data Structures                                         #####
################################################################################################################
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
    Classic = ThemeAttributes(
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
        border_left="  ",
        border_right="  ",
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