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
#import os as _os
#import sys as _sys
#import re as _re
#import string as _string
from AspireTUI._MESSAGES import current as _MSG
from AspireTUI import tui as _tui
from typing import Union as _Union
#################################################################################################################
#####                                           Class: LOG                                                  #####
#################################################################################################################
#
# 	Strings for internal use
#
from AspireTUI.Lists import LOG_LEVEL as LEVEL
from AspireTUI.Lists import LOG_SEVERITY as SEVERITY_TRANSLATED
_str_Title = "title"
_str_Desc = "desc"
_str_bUseDate = "bUseDate"
_str_bUseDateSections = "bUseDateSections"
_str_bUseTime = "bUseTime"
_str_bVerbose = "bVerbose"
_str_LL_ShowUser = "LL_ShowUser"
_str_LL_SaveLog = "LL_SaveLog"
_str_bTranslated = "bTranslated"
# English "pre-hardcoded"
SEVERITY[0] = "DEBUG"
SEVERITY[1] = "INFO"
SEVERITY[2] = "WARNING"
SEVERITY[3] = "ERROR"
SEVERITY[4] = "CRITICAL"
SEVERITY[5] = "FATAL"

# Prepare for class creation, obsolete because of import ? !
SEVERITY_TRANSLATED[0] = _MSG.cl_log_severity0
SEVERITY_TRANSLATED[1] = _MSG.cl_log_severity1
SEVERITY_TRANSLATED[2] = _MSG.cl_log_severity2
SEVERITY_TRANSLATED[3] = _MSG.cl_log_severity3
SEVERITY_TRANSLATED[4] = _MSG.cl_log_severity4
SEVERITY_TRANSLATED[5] = _MSG.cl_log_severity5


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
		self.Description = ""
		self.Title = ""
		self.bUseDate = False
		self.bUseDateSections = True
		self.bUseTime = True
		self.bVerbose = False
		self.LogLevel_ShowUser = 3
		self.LogLevel_SaveLog = 4
		self.Log_Format = "%H.%M.%S.%f"
		self.bTranslated = False
		# Get acccording strings:
		from AspireTUI.Lists import LOG_LEVEL as _LEVEL
		if self.bTranslated:
			from AspireTUI.Classes._Log import SEVERITY as _SEVERITY
			from AspireTUI.Lists import LOG_SEVERITY as _SEVERITY_TRANSLATED
			pass #self._b
		
		# Prepare get/set functions
		@property
		def Description(self):
			return self.Description
		@Description.setter
		def Description(self, new_val: str):
			msg = _MSG.cl_log_err_must_str
			if not isinstance(new_val, str):
				self.WARNING(msg)
				raise ValueError(msg)
			self.Description = new_val
		
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
	def __init__(self, filename: str, bVerbose=False, LOG_CONFIG=None, LOGFILE=None, ):
		
		""""
		Logfile Management Made Easy 			\n

		If you have a LOG_CONFIG, you do not need to provide a LOGFILE. \n
		
		from AspireTUI.FileUtils import log  	\n
		myLog = log( str_filename ) 			\n
		myLog.Settings.Title = "Title in new logfile"			\n
		myLog.Settings.LogLevel_ShowUser = myLog.LEVEL.WARNING	\n
		\n
		myConf.DEBUG(f"Only shown if myConf.Settings.LogLevel_ShowUser is: myConf.LEVEL.DEBUG")	\n
		\n
		SEVERITY[0] = "DEBUG" 		\n
		SEVERITY[1] = "INFO" 		\n
		SEVERITY[2] = "WARNING" 	\n
		SEVERITY[3] = "ERROR" 		\n
		SEVERITY[4] = "CRITICAL" 	\n
		SEVERITY[5] = "FATAL" 		\n
		"""		
		# Actual initialize class
		self.Filename = filename
		global LEVEL
		self.LEVEL = LEVEL.items
		for lvl in self.LEVEL:
			lvl._
			
		self.Settings = _Settings()

		# Prepare internal quick use:
		len_sev_max = 0
		if self.Settings.bTranslated:
			self._internal_severity_use = self.SEVERITY_TRANSLATED
		else:
			self._internal_severity_use = SEVERITY
		
		for lvl in LEVEL.items:
			# Get the right strings:
			sStr = self._internal_severity_use[lvl]				
			len_tmp = len(sStr)
			# Save new max value if current is longer
			if len_sev_max < len_tmp:
				len_sev_max = len_tmp
		# Now save longest count to attrtibue
		self._internal_indent_severity = len_sev_max
		
	#
	def _print_log(self, level: int, *args):
		"""
		INTERNAL:
		Check if a file needs to be opened
		"""
		# Simple things
		log_file = self.Filename
		iLen = self._internal_indent_severity
		
		# Prepare message from *args
		if 1 == len(*args):
			message = args[0]
		else:
			msg_str = args[0] 	;	args[0].remove()
			message = print(msg_str, *args)
		
		def __print_log_savefile(level:int, message=message, fn=log_file):
			prefix = self._in
			output = ""
			
			while open(fn, "a"):
				# TODO <---------------------------------------------------------
				pass

		# Show to user?
		if self.Settings.LogLevel_SaveLog >= level:
			_tui.status(111, message)
			#pass
		else:
			__print_log_savefile()
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
