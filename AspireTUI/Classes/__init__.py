"""
Description:
		Contains classes \n
		\n
		If file related, they are designed to be able to "emulate a file". \n
		This means, after reading a file (or None/"") nothing happens to the file, unless you save it. \n
		For LOG of course, this can be changed since you might have multiple instanced that access the file. \n
		\n

Usage:
		bVerbose = True 					# Show tui.status messages for each action to user
		                                    #
		from AspireTUI import Classes
		myLog = Classes.Log(filename_log, bVerbose=bVerbose )
		myConf = Classes.Conf(ini_config_file, bVerbose=bVerbose)
========================================================
Created on:		2024 Jan. 08
Created by:		Simon Arjuna Erat
License:		MIT
URL:			https://www.github.com/sri-arjuna/ASPIRE

Based on my TUI & SWARM for the BASH shell © 2011
"""
#################################################################################################################
#####                                           Simple structure for Classes                                #####
#################################################################################################################
"""
from AspireTUI.Classes._Conf import Conf
from AspireTUI.Classes._Log import Log
from AspireTUI.Classes._Crashlog import CrashLog
#from AspireTUI.Classes._App import AppManager
"""
from ._Conf import Conf
from ._Log import Log
from ._Crashlog import CrashLog
from ._AppManager import AppManager
