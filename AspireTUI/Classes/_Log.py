"""
	Description:
					Public functions to easy several tasks with Files
	Provides:
					from AspireTUI.Classes import Conf
					ret_bool, ret_str = cu.reg_value_get(file, key, var, bDual=True)
	Usage:
					from AspireTUI import Classes
					log = Classes.Log(log_file)
					log.settings.LogLevel_ShowUser =
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
#import os as _os
#import sys as _sys
#import re as _re
#import string as _string
from .. import _MSG
from .. import tui as _tui
from typing import Union as _Union

#
#	Strings for internal use
#
from ..Lists import LOG_LEVEL as LEVEL
from ..Lists import LOG_SEVERITY as SEVERITY

#################################################################################################################
#####                                           Class: LOG                                                  #####
#################################################################################################################
class Log:
	def __init__(self, 
		filename: str=None,
		name: str=None,
		iSaveLog: int=0,
		iShowUser: int=2,
		bVerbose: bool=False, 
		bAutoWrite: bool=True,
		bDaily: bool=False,
		comment: str=None,
		encoding: str="UTF-8",
		format = "%H.%M.%S.%f",
		config :str=None
		):
		
		""""
### Logfile Management Made Easy

__Basic Usage:__

    from AspireTUI import Classes
    log = Classes.Log("myApp.log", comment="Line 1 \nLine 2 \nLine 3... and so on")
    log.INFO("Logfile initialized")

Or you could do:

    from AspireTUI import Classes
    log = Classes.Log()
    log.INFO("Do your stuff")
    log.WARNING("Until its all done")
    log.save("my-log-session.log")

__Option Overview:__

	filename	\tExpects ".log", but if either cfg, ini or conf it will read that file instead, expecting this and the following values.

	bVerbose	\tThis will produce some AspireTUI output during creation of the log class

	bAutoWrite	\tThis toggles wether you write directly to the logfile or not. Default=True\n\t\tIf you want to save the messages, you will need to call:\n\t    log.

	iSaveLog	\tLogLevel at which messages will be shown to user

	iShowUser	\tLogLevel at which messages will be shown to user

	name    	\tShort string that can help identify which module has written the message

	comment 	\tStrings separated by \\n that will be printed on top of the new logfile as comments.

	encoding	\tDefault is UTF-8, should not be changed, but can if required.

from AspireTUI.Classes import Log  	\n
myLog = Log( str_filename ) 			\n
myLog.settings.Title = "Title in new logfile\nWith 2 heading comment lines"		\n
myLog.settings.LogLevel_ShowUser = myLog.LEVEL.WARNING	\n
myLog.save()			# Saves a config file of the log settings. \n
\n
myLog.DEBUG(f"Only shown if myLog.settings.LogLevel_ShowUser is: myLog.LEVEL.DEBUG")	\n
\n
SEVERITY[0] = "DEBUG" 		\n
SEVERITY[1] = "INFO" 		\n
SEVERITY[2] = "WARNING" 	\n
SEVERITY[3] = "ERROR" 		\n
SEVERITY[4] = "CRITICAL" 	\n
SEVERITY[5] = "FATAL" 		\n
		"""	
		#
		#	Prep Functions
		#
		def _SaveMessages(cls):
			"""
			If log.settings.bAutoWrite is False, all messages go to: log.messages

			Requires a log.settings.log.file or at least log.setting.name when using log.save()
			"""
			#global bAutoWrite
			if bAutoWrite:
				_tui.status(1, "autosafe chjeck on SaveMessages().... why?... and why twice?!")
			
		#
		#	Get sub menus
		#
		# Actual initialize class
		from . import _shared
		self.tools = _shared.SectionTools()
		self.settings = _shared.SectionSettings()
		_conf_file = None
		# Apply arguments
		self.settings.name = name
		self.settings.bAutoWrite = bAutoWrite
		self.settings.bVerbose = bVerbose
		self.settings.bDaily = bDaily
		self.settings.encoding = encoding
				
		#
		# 	Handle Filename
		# 
		if filename:
			# Has a filename to work with
			if filename.endswith(".log"):
				# default handling
				if bDaily:
					# Adjust name accordingly
					filename = filename.replace(".log", f"-{_tui._stew.date().replace('.','_')}.log")
			elif filename.endswith(".ini") or filename.endswith(".conf") or filename.endswith(".cfg"):
				# Its a config file
				_conf_file = filename
				self.settings.conf.file = _conf_file
				if name:
					# A name was passed, lets use that for the initial logfile
					filename = f"{name}.log"
		else:
			# No filename is passed, nothing will be written
			# This is a fallback method for some sort of "dynamic" output
			if bVerbose:
				_tui.status(LEVEL.INFO.value, "TODO: Filename (ini):", filename)
			else:
				self.settings.bAutoWrite = False
				if bVerbose:
					_tui.status(LEVEL.INFO.value, "Empty instance of AspireTui.Classes.Log" , "No logfile will be saved.")
		#
		# 	LOG
		#
		empty_list = []
		self.messages = empty_list
		#self.save = _SaveMessages(self)
		# Settings LOG
		self.settings.log.file = filename
		self.settings.log.format = format
		self.settings.log.comment = comment
		self.settings.log.level_ShowUser = iShowUser
		self.settings.log.level_SaveLog = iSaveLog
		
		len_sev_max = 0
		self._internal_severity_use = SEVERITY
		
		for lvl in LEVEL:
			# Get the right strings:
			sStr = self._internal_severity_use[lvl.value]				
			len_tmp = len(sStr)
			# Save new max value if current is longer
			if len_sev_max < len_tmp:
				len_sev_max = len_tmp
		# Now save longest count to attrtibue
		self._internal_indent_severity = len_sev_max
		
	def _has_header(cls, bDual=False):
		"""
		INTERNAL:

		Check if log file has the according content at the top of the file.

		If cls.settings.log.comment is None, it will return True regardless.

		If cls.settings.log.comment is given it will write the heading comment.
		"""
		if not cls.settings.log.comment:
			# As no header comment is provided, we can skip thi
			return True

		# Init
		this = cls.settings.log.file
		from AspireTUI.Path import exists as _exist
		ret_bool = False
		ret_msg = f"{_MSG.cl_conf_ui_reading}: {this}"
		# Check
		bExist = False
		if _exist(this):
			with open(this,"r", encoding=cls.settings.encoding) as fn:
				bExist = True
				fn.seek(0)
				if fn.readline(1) == "#":
					# File exists and a header comment exists
					ret_bool = True
				else:
					# File found, but has no header
					# Lets just verify there is a heading comment to be printed
					if cls.settings.log.comment:
						lines = []
						lines = cls.settings.log.comment.split("\n")
			if not ret_bool:	
				# File exists but has no header yet
				#print(f"# Created by: {cls.settings.title}, on {_tui._stew.now()}")
				with open(this, "w", encoding=cls.settings.encoding) as fn:
					for line in lines:
						print(f"# {line}", file=fn)
				ret_msg = f"Created log: \t{this}"
				# File exists and header written
				ret_bool = True
		else:
			# Files not found
			ret_bool = False
		# Return
		if bDual:
			return ret_bool, ret_msg
		else:
			ret_bool
		print("Exists: ", bExist)
		print("ret_bool: ", ret_bool, ret_msg)
	
	def _print_log(cls, level: int, *args):
	#def _print_log(cls, level: int, message: str, name: str=None,*args):
		"""
		INTERNAL:
		Check if a file needs to be opened
		"""
		# Simple things
		iLen = cls._internal_indent_severity
		iShow = cls.settings.log.level_ShowUser
		iSave = cls.settings.log.level_SaveLog
		log_file = cls.settings.log.file
		
		# Prepare message from *args
		if len(args) == 1:
			message = args[0]
		else:
			msg_str = args[0]
			message = msg_str % args[1:]
		# Actualy check if the header is required
		if cls._has_header(cls):
			print(f"Logfile: Detected header comment for logfile: {log_file}")
		else:
			print(f"Logfile: Written missing header comment for logfile: {log_file}")
		
		def __print_log_savefile(cls, level:int, message=message, fn=log_file, name: str=cls.settings.name, encoding=cls.settings.encoding):
			"""
			This saves a copy of the settings applied to the log settings.
			"""
			# Prepare output strings
			# Write: Date	Level	Type	Message
			from datetime import datetime as _datetime
			current_time = _datetime.now()
			formatted_time = current_time.strftime("%F_%H:%M:%S.%f")
			msg_out = f"{formatted_time}\t\t{level}\t{name}\t\t{message}"

			# Save outpout
			if cls.settings.bAutoWrite and fn is not None:
				with open(fn, 'at' , encoding=encoding) as thisLOG:
					print(f"{msg_out}", file=thisLOG)
			else:
				# Append to messages
				cls.messages.append(f"{msg_out}")
			return
		# Show to user?
		if level >= iShow:
			_tui.status(1000 + level, message)
		# Save to file?
		if level >= iSave:
			__print_log_savefile(cls, level, message, log_file)
	# 
	def DEBUG(self, *args):
		""""
		Show / Save message to user / file
		"""
		self._print_log(LEVEL.DEBUG.value, *args)

	def INFO(self, *args):
		""""
		Show / Save message to user / file
		"""
		self._print_log(LEVEL.INFO.value, *args)
	
	def WARNING(self, *args):
		""""
		Show / Save message to user / file
		"""
		self._print_log(LEVEL.WARNING.value, *args)
		
	def ERROR(self, *args):
		""""
		Show / Save message to user / file
		"""
		self._print_log(LEVEL.ERROR.value, *args)
	
	def CRITICAL(self, *args):
		""""
		Show / Save message to user / file
		"""
		self._print_log(LEVEL.CRITICAL.value, *args)
		
	def FATAL(self, *args):
		""""
		Show / Save message to user / file
		"""
		self._print_log(LEVEL.FATAL.value, *args)
