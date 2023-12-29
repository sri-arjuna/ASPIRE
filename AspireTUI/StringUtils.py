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
import os as _os
import sys as _sys
import re as _re
import string as _string
from datetime import datetime as _datetime
from AspireTUI import MESSAGE as _MSG
# 
#	Cross Platform & Advanced usage
#
import platform as _platform
import msvcrt as _msvcrt
import shutil as _shutil
import subprocess as _subprocess

#
#	Prepare data structures
#
from collections import namedtuple as _namedtuple
from dataclasses import dataclass as _dataclass


#################################################################################################################
#####                                           String Utils (stew)                                         #####
#################################################################################################################
def date(bNames=False):
	"""
	Returns date like:
	2024.12.30
	"""
	current_date = _datetime.now()
	formatted_date = current_date.strftime("%Y.%m.%d")
	if bNames:
		formatted_date += f" {current_date.strftime('%A, %B')}"
	return formatted_date

def time(bLong=False):
	"""
	Returns time like:
	15:30
	"""
	current_time = _datetime.now()
	formatted_time = current_time.strftime("%H:%M:%S")
	if bLong:
		formatted_time += f":{current_time.strftime('%S')}"
	return formatted_time

def now(clean=False, sep="/", bLong=False, bNames=False):
	"""
	Returns date and time like: \n
	2024.12.30 / 15:45
	"""
	if clean:
		return f"{date(bNames)} {time(bLong)}"
	else:
		return f"{date(bNames)} {sep} {time(bLong)}"

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
