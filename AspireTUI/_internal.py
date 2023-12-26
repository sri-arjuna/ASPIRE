"""
	Description:
					Internal functions for tui.*, handle string splitting and theme.
	
	Provides:
					put.border(style=header|title)			\n
					put.text(*args, style=header|title)

	========================================================
	Created on:		2023 Nov. 09
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE

	Based on my TUI & SWARM for the BASH shell © 2011
"""
################################################################################################################
#####                                            Shared Imports                                            #####
################################################################################################################
#
#	Essential imports
#
import AspireTUI.MESSAGE as _MSG
#import os as _os
#import sys as _sys
#import re as _re
#import string as _string
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
#from collections import namedtuple as _namedtuple
#from dataclasses import dataclass as _dataclass
from enum import Enum, EnumMeta as _Enum, _EnumMeta
#from typing import Union as _Union

################################################################################################################
#####                                            Error Handler                                             #####
################################################################################################################
#ERROR_MSG_THEME_NONE 		= f"_('You have not provided a proper theme.')"
ERROR_MSG_THEME_NONE 		=  #_("You have not provided a proper theme.")
ERROR_MSG_THEME_CANT_READ 	= # _("Cant read theme.")
ERROR_MSG_THEME_EMPTY_VAR	=  # _("The provided theme contains empty variables and can not be used!")
ERROR_MSG_COLOR_CANT_READ	= _("Cant read color code, please use plain text, not console code.")
ERROR_MSG_PRINT_COUNT		= _("You can only pass up to 3 strings as argument.")
ERROR_MSG_STATUS_ID			= _("The first argument to 'status' must be INT.")
ERROR_MSG_STATUS_COUNT		= _("You can only pass 2 string arguments to 'status' (= 3 with id).")

class _AspireErrorEnum(_Enum):
	THEME_NONE 			= _MSG.theme_none,
	THEME_CANT_READ 	= _MSG.theme_cant_read,
	THEME_EMPTY_VAR		= _MSG.theme_empty_var,
	COLOR_CANT_READ		= _MSG.theme_color_invalid,
	PRINT_COUNT			= _MSG.args_max3,
	STATUS_ID			= _MSG.args_status_first,
	STATUS_COUNT		= _MSG.args_2_status
class _AspireErrorSeverityEnum(_Enum):
	FATAL = _MSG.word_fatal,
	ERROR = _MSG.word_error

def ErrMsg(id: _AspireErrorEnum, severity: _AspireErrorSeverityEnum) -> str:
	print(severity + "\n" + id)
################################################################################################################
#####                                           String Utils (stew)                                        #####
################################################################################################################
def split_needed(txt_len: int, LineLength:int, percentage: int, style="print"):
	if txt_len >= LineLength:
		# Text is too long
		return True
	else:
		# Basicly, no split required, but there are exceptions
		# Specificly, if it is title, text should not be longer than 50 percentage (or the passed percentage)
		if style == "title" and 50 <= (LineLength / 100 * txt_len):
			return True
		return False
	
# Gets the char count at which it shall split the text
# Returns desired split position
def split_calc_char_pos(LineLength: int, Percentage: int):
	split_pos = 100 // LineLength * Percentage
	return split_pos

def split_string_preserve_words(text, max_chars):
	"""
	Split string at provided length, preferred at whitespace.
	Returns 2 strings: line0, line1
	"""
	words = text.split()
	line0 = ""
	current_length = 0
	rem_words = []
	# Parse each word
	for word in words:
		if current_length + len(word) <= max_chars:
			line0 += word + " "
			current_length += len(word) + 1  # Add 1 for space
			rem_words.append(word)
		else:
			break
	# Remove used words
	for w in rem_words:
		words.remove(w)
	# Fill line1
	line1 = text[current_length:].strip()
	return [line0.strip(), line1.strip()]

def shorten(txt: str, char_count: int, cut_from_middle: bool = False) -> str:
	"""
	Shorten text to fit into char_count, mostly used for tui.status.
	Optional: can shorten text in the middle of the string.
	"""
	if len(txt) <= char_count:
		return txt

	if cut_from_middle:
		# TODO: Why do i need another "- 10" and a "- 12"
		# Despite the fact i had already subtracted - 12 from in tui.progress...
		remaining_chars = char_count - 10 # org - 3, then 4...
		side_chars = int(remaining_chars // 2)
		shortened_text = f"{txt[:side_chars]}...{txt[-side_chars:]}"
	else:
		# Attempt to cut at word boundaries for better readability
		words = txt.split()
		shortened_words = []
		current_length = 0
		
		for word in words:
			if current_length + len(word) <= char_count - 12:	# org 3
				shortened_words.append(word)
				current_length += len(word) + 1  # Add 1 for space between words
		
		shortened_text = ' '.join(shortened_words)
		shortened_text += '...'  # Adding ellipsis
		
	return shortened_text
