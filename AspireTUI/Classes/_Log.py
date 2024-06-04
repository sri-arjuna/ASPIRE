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
#################################################################################################################
#####                                           Class: LOG                                                  #####
#################################################################################################################
#
# 	Strings for internal use
#
SEVERITY =[]
_SEVERITY_TRANSLATED = []
from ..Lists import LOG_LEVEL as LEVEL
from ..Lists import LOG_SEVERITY as SEVERITY


class _Settings:
	# Prepare get/set functions
	@property
	def description(self):
		return self.description
	@description.setter
	def description(self, new_val: str):
		msg = _MSG.cl_log_err_must_str
		if not isinstance(new_val, str):
			self.WARNING(msg)
			raise ValueError(msg)
		self.description = new_val

class Log:
	def __init__(self, 
		filename: str=None,
		bVerbose: bool=False, 
		bAutoSave: bool=True,
		iSaveLog: int=0,
		iShowUser: int=2,
		name: str=None,
		comment: str=None,
		encoding: str="UTF-8",
		format = "%H.%M.%S.%f"
		):
		
		""""
### Logfile Management Made Easy

__Basic Usage:__

    from AspireTUI import Classes
    logfile = "myApp.log"
    log = Classes.Log(logfile)
    log.header = "Line 1 \nLine 2 \nLine 3... and so on"
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

	bAutoSave	\tThis toggles wether you write directly to the logfile or not. Default=True\n\t\tIf you want to save the messages, you will need to call:\n\t    log.

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
			If log.settings.bAutoSave is False, all messages go to: log.messages

			Requires a log.settings.log.file or at least log.setting.name when using log.save()
			"""
			#global bAutoSave
			if bAutoSave:
				_tui.status(1, "autosafe chjeck on SaveMessages().... why?... and why twice?!")
			
		#
		#	Get sub menus
		#
		# Actual initialize class
		from . import _shared
		self.tools = _shared.SectionTools()
		self.settings = _shared.SectionSettings()
		# Apply arguments
		self.settings.name = name
		self.settings.bAutoSave = bAutoSave
		self.settings.bVerbose = bVerbose
		self.settings.encoding = encoding
				
		# Set filename at the proper place
		if filename.endswith(".log"):
			self.settings.log.file = filename
			if bVerbose:
				_tui.status(LEVEL.INFO.value, "Filename (log):", filename)
		elif filename.endswith(".cfg", ".conf", ".ini"):
			self.settings.conf.file = filename
			if bVerbose:
				_tui.status(LEVEL.INFO.value, "Filename (ini):", filename)
		else:
			_tui.status(False, "Could not identify logfile:", filename)
		
		# LOG
		empty_list = []
		self.messages = empty_list
		#self.save = _SaveMessages(self)
		# Settings LOG
		self.settings.log.file = filename
		self.settings.log.format = format
		self.settings.log.comment = comment
		self.settings.log.level_ShowUser = iShowUser
		self.settings.log.level_SaveLog = iSaveLog
		
		#self.settings.LOG_CONFIG = 

		#global LEVEL
		#self.LEVEL = LEVEL
		#for lvl in self.LEVEL:
	#		lvl._
			
		
		#if self.settings.bTranslated:
		#	self._SEVERITY_USE = _MSG._SEVERITY_TRANSLATED
		#else:
		#	self._SEVERITY_USE = SEVERITY

		# Prepare internal quick use:
		len_sev_max = 0
		#if self.settings.bTranslated:
		#	self._internal_severity_use = self.SEVERITY_TRANSLATED
		#else:
		#	self._internal_severity_use = SEVERITY
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
		- Title
		- Description 		WIP <--------
		"""
		# Init
		this = cls.settings.log.file
		from AspireTUI.Path import exists as _exist
		ret_bool = False
		ret_msg = f"{_MSG.cl_conf_ui_reading}: {this}"
		# Check
		if _exist(this):
			bExist = False
			with open(this,"r", encoding=cls.settings.encoding) as fn:
				bExist = True
				if fn.readline(1) == "#":
					# File exists and a header comment exists
					ret_bool = True
				else:
					# File found, but has no header
					lines = []
					lines = cls.settings.log.comment.split("\n")
			if bExist and not ret_bool:	
				# File exists but has no header yet
				#print(f"# Created by: {cls.settings.title}, on {_tui._stew.now()}")
				with open(this, "w", encoding=cls.settings.encoding) as fn:
					for line in lines:
						print(f"# {line}", file=fn)
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
		cls._has_header()
		
		def __print_log_savefile(cls, level:int, message=message, fn=log_file, name: str=cls.settings.name, encoding=cls.settings.encoding):
			"""
			This saves a copy of the settings applied to the log settings.
			"""
			if cls.settings.bAutoSave:
				with open(fn, 'at' , encoding=encoding) as thisLOG:
					# Write: Date	Level	Type	Message
					from datetime import datetime as _datetime
					current_time = _datetime.now()
					formatted_time = current_time.strftime("%F_%H:%M:%S.%f")
					print(f"{formatted_time}\t\t{level}\t{name}\t\t{message}", file=thisLOG)
			else:
				# Append to messages
				cls.messages.append("TODO")
			return
		# Show to user?
		if level >= iShow:
			_tui.status(1000 + level, message)
		# Save to file?
		if level >= iSave:
			__print_log_savefile(cls, level, message)
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
