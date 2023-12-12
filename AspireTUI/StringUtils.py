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
