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

_str_Title = "title"
_str_Desc = "desc"
_str_bUseDate = "bUseDate"
_str_bUseDateSections = "bUseDateSections"
_str_bUseTime = "bUseTime"
_str_bVerbose = "bVerbose"
_str_LL_ShowUser = "LL_ShowUser"
_str_LL_SaveLog = "LL_SaveLog"
_str_bTranslated = "bTranslated"

# English "pre-hardcoded" - obsolete because of import ? ! -- when/if it works
#_SEVERITY[]
#SEVERITY[0] = "DEBUG"
#SEVERITY[1] = "INFO"
#SEVERITY[2] = "WARNING"
#SEVERITY[3] = "ERROR"
#SEVERITY[4] = "CRITICAL"
#SEVERITY[5] = "FATAL"

# Prepare for class creation, this is required


#_str_ = ""
#
#	
#
class _Settings:
	def __init__(self):
		"""
		Settings of the LOG file
		"""
		# Set default values
		self.filename = ""
		self.description = ""
		self.title = ""
		self.bUseDate = False
		self.bUseDateSections = True
		self.bUseTime = True
		self.bVerbose = False
		self.LogLevel_ShowUser = 3
		self.LogLevel_SaveLog = 4
		self.Log_Format = "%H.%M.%S.%f"
		self.bTranslated = False
		# Get acccording strings:
		from ..Lists import LOG_LEVEL as _LEVEL
		
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
		
		@property
		def title(self):
			return self.title
		@title.setter
		def title(self, new_val: str):
			msg = _MSG.cl_log_err_must_str
			if not isinstance(new_val, str):
				self.WARNING(msg)
				raise ValueError(msg)
			self.title = new_val

		@property
		def bUseDate(self):
			return self.bUseDate
		@bUseDate.setter
		def bUseDate(self, new_val: bool):
			msg = _MSG.cl_log_err_must_bool
			if not isinstance(new_val, bool):
				self.WARNING(msg)
				raise ValueError(msg)
			self.bUseDate = new_val
		
		@property
		def bUseDateSections(self):
			return self.bUseDateSections
		@bUseDateSections.setter
		def bUseDateSections(self, new_val: bool):
			msg = _MSG.cl_log_err_must_bool
			if not isinstance(new_val, bool):
				self.WARNING(msg)
				raise ValueError(msg)
			self.bUseDateSections = new_val
		
		@property
		def bUseTime(self):
			return self.bUseTime
		@bUseTime.setter
		def bUseTime(self, new_val: bool):
			msg = _MSG.cl_log_err_must_bool
			if not isinstance(new_val, bool):
				self.WARNING(msg)
				raise ValueError(msg)
			self.bUseTime = new_val
		
		@property
		def bVerbose(self):
			return self.bVerbose
		@bVerbose.setter
		def bVerbose(self, new_val: bool):
			msg = _MSG.cl_log_err_must_bool
			if not isinstance(new_val, bool):
				self.WARNING(msg)
				raise ValueError(msg)
			self.bVerbose = new_val

class Log:
	def __init__(self, filename: str, bVerbose=False, bDual=False ):
		
		""""
		Logfile Management Made Easy 			\n

		if filename is a '.log' file, and no log.settings are changed, default settings will be used. \n
		If filename is a conf/ini file, it will try to apply those values to the settings. \n
		If no filename (LOG_CONFIG) could be found (on safe)

		Those are: \n
		* log level - show user = 3 warning = 3+
		* log level - save to log = 4 error = 4+



		If you have a LOG_CONFIG, you do not need to provide a LOGFILE. \n
		
		from AspireTUI.Classes import Log  	\n
		myLog = Log( str_filename ) 			\n
		myLog.settings.Title = "Title in new logfile"			\n
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
		# Actual initialize class
		self.settings = _Settings()
		self.settings.filename = filename
		self.settings.bVerbose = bVerbose
		#self.settings.LOG_CONFIG = 

		#global LEVEL
		#self.LEVEL = LEVEL
		#for lvl in self.LEVEL:
	#		lvl._
			
		
		if self.settings.bTranslated:
			self._SEVERITY_USE = _MSG._SEVERITY_TRANSLATED
		else:
			self._SEVERITY_USE = SEVERITY

		# Prepare internal quick use:
		len_sev_max = 0
		if self.settings.bTranslated:
			self._internal_severity_use = self.SEVERITY_TRANSLATED
		else:
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
		this = cls.settings.filename
		from AspireTUI.Path import exists as _exist
		ret_bool = False
		ret_msg = f"{_MSG.cl_conf_ui_reading}: {this}"
		# Check
		if _exist(this):
			with open(this,"r", encoding="UTF-8") as fn:
				pass
			# File exists and header verified (TODO)
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
		"""
		INTERNAL:
		Check if a file needs to be opened
		"""
		# Simple things
		log_file = cls.settings.filename
		iLen = cls._internal_indent_severity
		
		# Prepare message from *args
		if len(args) == 1:
			message = args[0]
		else:
			msg_str = args[0]
			message = msg_str % args[1:]
		# Actualy check if the header is required
		cls._has_header()
		
		def __print_log_savefile(cls, level:int, message=message, fn=log_file):
			"""
			This saves a copy of the settings applied to the log settings.
			"""
			print(cls.settings.LogLevel_SaveLog)
			return
			"""
			prefix = cls.settings
			output = ""
			
			while open(fn, "a"):
				# TODO <---------------------------------------------------------
				pass
			"""

		# Show to user?
		if cls.settings.LogLevel_ShowUser >= level:
			_tui.status(1000 + level, message)
			#pass
		if cls.settings.LogLevel_SaveLog >= level:
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
