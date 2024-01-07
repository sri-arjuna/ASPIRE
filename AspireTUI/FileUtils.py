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
from . import MESSAGE as _MSG
from . import tui as _tui
from typing import Union as _Union
#################################################################################################################
#####                                           Class: LOG                                                  #####
#################################################################################################################
#
# 	Strings for internal use
#
_str_Title = "title"
_str_Desc = "desc"
_str_bUseDate = "bUseDate"
_str_bUseDateSections = "bUseDateSections"
_str_bUseTime = "bUseTime"
_str_bVerbose = "bVerbose"
_str_LL_ShowUser = "LL_ShowUser"
_str_LL_SaveLog = "LL_SaveLog"
_str_bTranslated = "bTranslated"

LEVEL = {
	"DEBUG":	0,
	"INFO": 	1,
	"WARNING":	2,
	"ERROR":	3,
	"CRITICAL":	4,
	"FATAL":	5
}
SEVERITY[0] = "DEBUG"
SEVERITY[1] = "INFO"
SEVERITY[2] = "WARNING"
SEVERITY[3] = "ERROR"
SEVERITY[4] = "CRITICAL"
SEVERITY[5] = "FATAL"


_severity_translated[0] = _MSG.cl_log_severity0
_severity_translated[1] = _MSG.cl_log_severity1
_severity_translated[2] = _MSG.cl_log_severity2
_severity_translated[3] = _MSG.cl_log_severity3
_severity_translated[4] = _MSG.cl_log_severity4
_severity_translated[5] = _MSG.cl_log_severity5


#_str_ = ""
#
#	
#
class Settings:
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
		self.bTranslated = False
		
		# Prepare get/set functions
		@property
		def desc(self):
			return self.desc
		@desc.setter
		def desc(self, new_val: str):
			msg = _MSG.cl_log_err_must_str
			if not isinstance(new_val, str):
				self.WARNING(msg)
				raise ValueError(msg)
			self.desc = new_val
		
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

class log:
	def __init__(self, filename: _Union[str,]):
		
		""""
		Logfile Management Made Easy 			\n

		from AspireTUI.FileUtils import log  	\n
		prj_log = log( str_filename ) 			\n
		prj_log.Settings.Title = "Title in new logfile"			\n
		prj_log.Settings.LogLevel_ShowUser = log.LEVEL.WARNING	\n
		prj_log.DEBUG(f"Only shown if LogLevel_ShowUser is {prj_log.Settings.LogLevel_ShowUser}")	\n

		SEVERITY[0] = "DEBUG" 		\n
		SEVERITY[1] = "INFO" 		\n
		SEVERITY[2] = "WARNING" 	\n
		SEVERITY[3] = "ERROR" 		\n
		SEVERITY[4] = "CRITICAL" 	\n
		SEVERITY[5] = "FATAL" 		\n
		"""		
		# Actual initialize class
		self.Filename = filename
		self.Settings = Settings()

		# Prepare internal quick use:
		global SEVERITY
		self._internal_severity_eng = SEVERITY
		self._internal_severity_translated = _severity_translated
		len_sev_max = 0
		if self.Settings.bTranslated:
			self._internal_severity_use = _severity_translated
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
	def _print_log(self, level: int, *args)
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
			
			

			while open(fn, "a")
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
