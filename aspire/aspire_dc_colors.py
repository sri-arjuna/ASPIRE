"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""


from dataclasses import dataclass


@dataclass
class TextCodes:
	reset: str = '\033[0m'
	bold: str = '\033[1m'
	italic: str = '\033[3m'
	underline: str = '\033[4m'
	invert: str = '\033[7m'
	blink: str = '\033[5m'
	line_up: str = '\033[1A'
	line_down: str = '\033[1B'


@dataclass
class ColorsForeground:
	reset: str = '\033[39m'
	black: str = '\033[30m'
	red: str = '\033[31m'
	green: str = '\033[32m'
	yellow: str = '\033[33m'
	blue: str = '\033[34m'
	magenta: str = '\033[35m'
	cyan: str = '\033[36m'
	light_gray: str = '\033[37m'
	dark_gray: str = '\033[90m'
	light_red: str = '\033[91m'
	light_green: str = '\033[92m'
	light_yellow: str = '\033[93m'
	light_blue: str = '\033[94m'
	light_magenta: str = '\033[95m'
	light_cyan: str = '\033[96m'
	white: str = '\033[97m'


@dataclass
class ColorsBackground:
	reset: str = '\033[49m'
	black: str = '\033[40m'
	red: str = '\033[41m'
	green: str = '\033[42m'
	yellow: str = '\033[43m'
	blue: str = '\033[44m'
	magenta: str = '\033[45m'
	cyan: str = '\033[46m'
	light_gray: str = '\033[47m'
	dark_gray: str = '\033[100m'
	light_red: str = '\033[101m'
	light_green: str = '\033[102m'
	light_yellow: str = '\033[103m'
	light_blue: str = '\033[104m'
	light_magenta: str = '\033[105m'
	light_cyan: str = '\033[106m'
	white: str = '\033[107m'
