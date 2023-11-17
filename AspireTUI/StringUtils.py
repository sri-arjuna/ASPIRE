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
import os
import sys
import re
import string
from datetime import datetime
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

#################################################################################################################
#####                                           String Utils (stew)                                         #####
#################################################################################################################
def date():
	current_date = datetime.now()
	formatted_date = current_date.strftime("%Y.%m.%d")
	return formatted_date

def time():
	current_time = datetime.now()
	formatted_time = current_time.strftime("%H:%M:%S")
	return formatted_time

def now(clean=False, sep="/"):
	if clean:
		return f"{date()} {time()}"
	else:
		return f"{date()} {sep} {time()}"

def shorten(txt: str, char_count: int, cut_from_middle: bool = False) -> str:
	"""
	Shorten text to fit into char_count, mostly used for tui.status.
	Optional: can shorten text in the middle of the string.
	"""
	if len(txt) <= char_count:
		return txt

	if cut_from_middle:
		remaining_chars = char_count - 3
		side_chars = remaining_chars // 2
		shortened_text = f"{txt[:side_chars]}...{txt[-side_chars:]}"
	else:
		words = txt.split()
		total_len = 0
		shortened_words = []
		for word in words:
			total_len += len(word)
			if total_len > char_count - 3:
				break
			shortened_words.append(word)
		
		shortened_text = ' '.join(shortened_words) + '...'

	return shortened_text

