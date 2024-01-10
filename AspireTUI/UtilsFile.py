"""
	Description:
					Public functions to easy several tasks with Files
	Provides:
					from AspireTUI import ConfigUtills as cu
					ret_bool, ret_str = cu.reg_value_get(file,key,var)
					
	========================================================
	Created on:		2024 Jan. 01
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
#import re as _re
#import string as _string
from . import MESSAGE as _MSG
from . import tui as _tui
from typing import Union as _Union
################################################################################################################
#####                                            Basic Checks                                              #####
################################################################################################################
def file_exists(filename: FileDescriptorOrPath, bVerbose=False):
	"""
	Returns True if filename exists.
	"""
	if bVerbose:
		if _os.path.exists(filename):
			_tui.status(True, _MSG.)
