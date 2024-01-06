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
		# Prepare get/set functions
		def _desc(new_Desc = None) -> str:
			"""
			Get or Set a str
			"""
			if new_Desc not None:
				self.Description = new_Desc
				self._current_config[_str_Desc] = new_Desc
			else:
				return self._current_config[_str_Desc]
		def _title(new_Title = None) -> str:
			"""
			Get or Set a str
			"""
			if new_Title not None:
				self.Title = new_Title
				self._current_config[_str_Title] = new_Title
			else:
				return self._current_config[_str_Title]
		def _bUseDate(new_Val = None) -> bool:
			"""
			Get or Set a bool
			"""
			if new_Val not None:
				self.bUseDate = new_Val
				self._current_config[_str_bUseDate] = new_Val
			else:
				return self._current_config[_str_bUseDate]
		def _bUseDateSections(new_Val = None) -> bool:
			"""
			Get or Set a bool
			"""
			if new_Val not None:
				self.bUseDateSections = new_Val
				self._current_config[_str_bUseDateSections] = new_Val
			else:
				return self._current_config[_str_bUseDateSections]
		def _bUseTime(new_Val = None) -> bool:
			"""
			Get or Set a bool
			"""
			if new_Val not None:
				self.bUseTime = new_Val
				self._current_config[_str_bUseTime] = new_Val
			else:
				return self._current_config[_str_bUseTime]
		def _bVerbose(new_Val = None) -> bool:
			"""
			Get or Set a bool
			"""
			if new_Val not None:
				self.bbVerbose = new_Val
				self._current_config[_str_bVerbose] = new_Val
			else:
				return bool(self._current_config[_str_bVerbose])
		def _LogLevel_ShowUser(new_Val = None) -> int:
			"""
			Get or Set an int
			"""
			if new_Val not None:
				self.LogLevel_ShowUser = new_Val
				self._current_config[_str_LL_ShowUser] = new_Val
			else:
				return self._current_config[_str_LL_ShowUser]
		def _LogLevel_SaveLog(new_Val = None) -> int:
			"""
			Get or Set an int
			"""
			if new_Val not None:
				self.LogLevel_SaveLog = new_Val
				self._current_config[_str_LL_SaveLog] = new_Val
			else:
				return self._current_config[_str_LL_SaveLog]
		def _bTranslated(new_Val = None) -> bool:
			"""
			Get or Set a bool
			"""
			if new_Val not None:
				self.LogLevel_SaveLog = new_Val
				self._current_config[_str_LL_SaveLog] = new_Val
			else:
				return self._current_config[_str_LL_SaveLog]
		
		# Actualy assign functions to attributes
		self.Description = _desc()
		self.Title = _title()
		self.bUseDate = _bUseDate()
		self.bUseDateSections = _bUseDateSections()
		self.bUseTime = _bUseTime()
		self.bVerbose = _bVerbose()
		self.LogLevel_ShowUser = _LogLevel_ShowUser()
		self.LogLevel_SaveLog = _LogLevel_SaveLog()
		self.bTranslated = _bTranslated()

		@property
		def desc(self):
			return self.desc
		
		@desc.setter
		def desc(self, new_desc: str):
			if not isinstance(new_desc, str):
				self.WARNING(_MSG.cl_log_err_must_str)
				raise ValueError(_MSG.cl_log_err_must_str)
			# Add additional validation logic if needed
			self.desc = new_desc

class log:
	def __init__(self, filename: _Union[str,]):
		
		""""
		Logfile Management Made Easy 			\n

		from AspireTUI.FileUtils import log  	\n
		prj_log = log( str_filename ) 			\n
		prj_log.Settings.Title = "Title in new logfile"			\n
		prj_log.Settings.LogLevel_ShowUser = log.LEVEL.WARNING	\n
		prj_log.DEBUG("Only shown if LogLevel_ShowUser is 0")	\n

		SEVERITY[0] = "DEBUG" 		\n
		SEVERITY[1] = "INFO" 		\n
		SEVERITY[2] = "WARNING" 	\n
		SEVERITY[3] = "ERROR" 		\n
		SEVERITY[4] = "CRITICAL" 	\n
		SEVERITY[5] = "FATAL" 		\n
		"""
		# Prepare default values:
		self._current_config[_str_Title] = ""
		self._current_config[_str_Desc] = ""
		self._current_config[_str_bUseDate] = False
		self._current_config[_str_bUseDateSections] = True
		self._current_config[_str_bUseTime] = True
		self._current_config[_str_bVerbose] = False
		self._current_config[_str_LL_ShowUser] = 3
		self._current_config[_str_LL_SaveLog] = 1
		self._current_config[_str_bTranslated] = False
		
		# Actual initialize class
		self.Filename = filename
		self.Settings = Settings()

		# Prepare internal quick use:
		global SEVERITY
		self._internal_severity_eng = SEVERITY
		self._internal_severity_translated = _severity_translated
		len_sev_max = 0
		for lvl in LEVEL.items:
			# Get the right strings:
			if self._current_config[_str_bTranslated] == True:
				sStr = _severity_translated[lvl]
			else:
				sStr = SEVERITY[lvl]
			len_tmp = len(sStr)
			# Save new max value if current is longer
			if len_sev_max < len_tmp:
				len_sev_max = len_tmp
		# Now save longest count to attrtibue
		self._internal_indent_severity = len_sev_max


		
	#
	def _print_log(self, level: int, message: str)
		"""
		INTERNAL:
		Check if a file needs to be opened
		"""
		log_file = self.Filename

		if self.Settings.LogLevel_SaveLog >= level:
			

	# 
	def DEBUG(self, message: str):
		""""
		Shows / Saves message to user / file
		"""
		# Prepare message
		#message = *args.join()
		message = print(*args.join())
		
		# Show to user?
		if self.Settings.bVerbose or self.Settings.LogLevel_ShowUser >= LEVEL.DEBUG.value:
			_tui.status(111, message)
		# Save to Log?
		
			self._print_log(LEVEL.DEBUG.value, message)
	
