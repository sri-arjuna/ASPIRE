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
def date():
	current_date = _datetime.now()
	formatted_date = current_date.strftime("%Y.%m.%d")
	return formatted_date

def time():
	current_time = _datetime.now()
	formatted_time = current_time.strftime("%H:%M:%S")
	return formatted_time

def now(clean=False, sep="/"):
	if clean:
		return f"{date()} {time()}"
	else:
		return f"{date()} {sep} {time()}"

