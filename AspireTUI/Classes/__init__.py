"""
Description:
		Contains classes
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
from Classes._Conf import Conf
from Classes._Log import Log
from Classes._Crashlog import CrashLog
