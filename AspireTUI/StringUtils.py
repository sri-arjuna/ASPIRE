"""
	Description:
					Public functions to easy several tasks with strings (or math)
	Provides:
					from AspireTUI import StringUtills as stew
					stew.date() , stew.time()
					
	========================================================
	Created on:		2023 Nov. 09
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE

	Based on my TUI & SWARM for the BASH shell © 2011
"""
#
#	Essential imports
#
#import os as _os
#import sys as _sys
import re as _re
#import string as _string
from datetime import datetime as _datetime
#from AspireTUI import MESSAGE as _MSG
# 
#	Cross Platform & Advanced usage
#
#import platform as _platform
#import msvcrt as _msvcrt
#import shutil as _shutil
#import subprocess as _subprocess

#
#	Prepare data structures
#
from collections import namedtuple as _namedtuple
from dataclasses import dataclass as _dataclass
from typing import Union as _Union
#
#	Internal imports
#
from . import MESSAGE as _MSG

#################################################################################################################
#####                                           String Utils (stew)                                         #####
#################################################################################################################
def date(bNames=False) -> str:
	"""
	Returns date like:
	2024.12.30
	"""
	current_date = _datetime.now()
	formatted_date = current_date.strftime("%Y.%m.%d")
	if bNames:
		formatted_date += f" {current_date.strftime('%A, %B')}"
	return formatted_date

def time(bLong=False) -> str:
	"""
	Returns time like:
	15:30
	"""
	current_time = _datetime.now()
	formatted_time = current_time.strftime("%H:%M:%S")
	if bLong:
		formatted_time += f":{current_time.strftime('%S')}"
	return formatted_time

def now(clean=False, sep="/", bLong=False, bNames=False) -> str:
	"""
	Returns date and time like: \n
	2024.12.30 / 15:45
	"""
	if clean:
		return f"{date(bNames)} {time(bLong)}"
	else:
		return f"{date(bNames)} {sep} {time(bLong)}"

def logtime() -> str:
	"""
	Returns a string to be used for safe-file-names.
	"""
	current_time = _datetime.now()
	formatted_time = current_time.strftime("%Y.%m.%d_%H.%M.%S")
	return formatted_time

def close_html_tags(html_string: str, exclude="") -> str:
	"""
	Close open HTML tags in the provided string.
	Exclude closing "<div>" tags.
	"""
	# Match open tags
	open_tags = _re.findall(r'<([^/][^>]*)>', html_string)

	# Check for open tags from the end of the string
	for tag in reversed(open_tags):
		if exclude:
			if not tag.startswith(exclude):
				# Close the tag
				html_string += f'</{tag}>'
		else:
			html_string += f'</{tag}>'
	# No treatment required 
	return html_string

def esc2hex(strESC:str) -> str:
	"""
	Transforms internal color codes to web-hex-colors. \n
	Returns an empty string if it didnt find something to close. \n
	Example: colorA = esc2hex(cat.fg.white)
	"""
	from AspireTUI.ColorAndText import cat as _cat
	if strESC == _cat.reset:
		# Handle special case for cat.reset
		return close_html_tags(strESC)
	elif _re.match(r'<color=[^>]+>', strESC):
			# Fallback: Close color tags
			return _re.sub(r'<color=[^>]+>', '</color>', strESC)
	return ""

def conf2dict(config_string) -> dict:
	"""
	Splits the content of a conf file, or env/set outputs to a dictionary
	"""
	tmp_dict = {}
	for line in config_string.split('\n'):
		if '=' in line:
			key, value = line.split('=', 1)
			tmp_dict[key] = value
	return tmp_dict

def sec2time(sec:_Union[int, float], format=None) -> str:
	"""
	Transforms given seconds to proper HH:MM:SS format.
	"""
	if isinstance(sec, int):
		# Default, basic seconds
		format_fmt = "%H:%M:%S"
	elif isinstance(sec, float):
		# It is microseconds
		format_fmt = "%H:%M:%S.%f"
	else:
		# Unsupported
		raise ValueError(_MSG.word_error, _MSG.cl_log_err_must_int, _MSG.cl_log_err_must_float)

	# Prefer passed format over default
	if format is None:
		format = format_fmt

	# Return passed seconds as time according to format
	return _datetime.datetime.utcfromtimestamp(sec).strftime(format)

def num2roman(num: int) -> chr:
	"""
	Converts an integer to Roman numeral
	"""
	if not 0 < num:
		raise ValueError("Input must be a positive integer")
	
	from AspireTUI import Lists as _lists
	roman_numerals = _lists.roman_num2roman
	result = ''
	for value, numeral in roman_numerals.items():
		count = num // value
		result += numeral * count
		num %= value

	return result

def roman2num(roman: str) -> int:
	"""
	Converts Roman numeral to integer
	"""
	from AspireTUI import Lists as _lists
	roman_numerals = _lists.roman_roman2num

	result = 0
	prev_value = 0

	for numeral in reversed(roman):
		value = roman_numerals[numeral]
		if value < prev_value:
			result -= value
		else:
			result += value
		prev_value = value

	return result

def char2morse(input_data):
	"""
	Converts characters or a multiline string to Morse code.
	"""
	from AspireTUI.Lists import morse_code as _MORSE_CODE_DICT
	if isinstance(input_data, str):
		input_data = input_data.upper().splitlines()
	return '\n'.join([' '.join([_MORSE_CODE_DICT[char] if char in _MORSE_CODE_DICT else char for char in line]) for line in input_data])

def morse2char(input_data):
	"""
	Converts Morse code to characters.
	"""
	from AspireTUI.Lists import morse_code as _MORSE_CODE_DICT
	if isinstance(input_data, str):
		input_data = input_data.splitlines()
	morse_dict_reverse = {value: key for key, value in _MORSE_CODE_DICT.items()}
	return '\n'.join([''.join([morse_dict_reverse[code] if code in morse_dict_reverse else code for code in line.split()]) for line in input_data])
