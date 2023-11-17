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
import os
import sys
import re
import string
#
#	Cross Platform & Advanced usage
#
import platform
import msvcrt
import shutil
import subprocess
#
#	Prepare data structures
#
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum, EnumMeta
#
#	Prepare for multi language support
#
import gettext #as _
from pathlib import Path
# Lang setup
translation_directory = Path("locales")
translation = gettext.translation("AspireTUI", translation_directory, fallback=True)
translation.install()
################################################################################################################
#####                                            Error Handler                                             #####
################################################################################################################
#ERROR_MSG_THEME_NONE 		= f"_('You have not provided a proper theme.')"
ERROR_MSG_THEME_NONE 		= _("You have not provided a proper theme.")
ERROR_MSG_THEME_CANT_READ 	= _("Cant read theme.")
ERROR_MSG_THEME_EMPTY_VAR	= _("The provided theme contains empty variables and can not be used!")
ERROR_MSG_COLOR_CANT_READ	= _("Cant read color code, please use plain text, not console code.")
ERROR_MSG_PRINT_COUNT		= _("You can only pass up to 3 strings as argument.")
ERROR_MSG_STATUS_ID			= _("The first argument to 'status' must be INT.")
ERROR_MSG_STATUS_COUNT		= _("You can only pass 2 string arguments to 'status' (= 3 with id).")

class _AspireErrorEnum(Enum):
	THEME_NONE 			= ERROR_MSG_THEME_NONE,
	THEME_CANT_READ 	= ERROR_MSG_THEME_CANT_READ,
	THEME_EMPTY_VAR		= ERROR_MSG_THEME_EMPTY_VAR,
	COLOR_CANT_READ		= ERROR_MSG_COLOR_CANT_READ,
	PRINT_COUNT			= ERROR_MSG_PRINT_COUNT,
	STATUS_ID			= ERROR_MSG_STATUS_ID,
	STATUS_COUNT		= ERROR_MSG_STATUS_COUNT

def ErrMsg(id: _AspireErrorEnum) -> str:
	str_type = _("Fatal")
	print(str_type + "\n" + id)
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

# Split string at provided percentage
# prfered at white space, or if not possible, hard value
def split_string_preserve_words(text, max_chars):
	total_length = len(text)
	
	if total_length <= max_chars:
		return [text.strip(), ""]
	
	# Find the nearest whitespace before or at the max_chars index
	split_index = max_chars
	while split_index > 0 and not text[split_index].isspace():
		split_index -= 1
	
	# If we didn't find a whitespace, just split at the provided index
	if split_index == 0:
		split_index = max_chars
	
	line0 = text[:split_index].strip()
	line1 = text[split_index:].strip()
	
	# If line0 or line1 is empty, consider splitting the string without preserving words
	if not line0 or not line1:
		split_index = max_chars
		line0 = text[:split_index].strip()
		line1 = text[split_index:].strip()
	
	return [line0, line1]

def shorten(txt: str, char_count: int, cut_from_middle: bool = False) -> str:
	"""
	Shorten text to fit into char_count, mostly used for tui.status.
	optional: can shorten text in the middle of the string.
	"""
	if len(txt) <= char_count:
		return txt

	if cut_from_middle:
		if char_count < 7:
			return "..." + txt[-(char_count - 3):]

		middle = len(txt) // 2
		offset = (char_count - 3) // 2
		start_index = middle - offset
		end_index = middle + offset + 1 if char_count % 2 != 0 else middle + offset

		shortened_text = f"{txt[:start_index]}...{txt[end_index:]}"
		return shortened_text
	else:
		# Split text into words and calculate the length of each word
		words = txt.split()
		lengths = [len(word) for word in words]

		# Construct the shortened text by taking whole words until char_count is reached
		shortened_text = ""
		current_length = 0
		for word, length in zip(words, lengths):
			if current_length + length <= char_count - 3:
				shortened_text += f"{word} "
				current_length += length + 1  # Add 1 for the space after the word
			else:
				break
		
		# If the shortened text doesn't match the input text length, add '...' at the end
		if len(shortened_text) < len(txt):
			shortened_text += "..."

		return shortened_text.rstrip()

