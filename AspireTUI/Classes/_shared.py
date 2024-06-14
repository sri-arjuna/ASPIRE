"""
Description:
		Class: 	Classes/_shared
		Detail:	Provides functions used by the actual classes for tool access and generic class settings/configuration.


Notes:
		If a LOG_CONFIG= is passed and the file exists, it will be read.
		If it does not exist, the default/passed settings will be written into LOG_CONFIG
		See: myLog.settings for details.
========================================================
Created on:		2024 Jun. 03
Created by:		Simon Arjuna Erat
License:		MIT
URL:			https://www.github.com/sri-arjuna/AspireTUI

Based on my TUI & SWARM for the BASH shell © 2011
"""
#
#	Imports
#
from .._MESSAGES import current as _MSG

#
#	Shared functions
#
# Prepare generic settings
class SectionSettings():
	def __init__(self):
		"""
		Provides basic settings for LOG and CONF classes 	\n
		Values need to be set from its parent class.
		"""
		class _subLog:
			# Contains values related to logs
			file = None
			level_ShowUser = 2
			level_SaveLog = 0
			format = "%H.%M.%S.%f"
			comment = ""
			bDaily = True

		class _subConf:
			# Contains values related to conf - config
			file = None
			sections = "[]"
			value_sep = "="
			comment = ""

		# Name of the actual conf or log file
		self.conf = _subConf()
		self.log = _subLog()
		self.name = None
		#self.comment = None
		self.bAutoSave = False
		self.bVerbose = False
		self.bDaily = False
		self.encoding = "UTF-8"

# Prepare tools
class SectionTools():
	"""
	Provides easy access ti basic tools like tui and lists
	These are used from within the class
	"""
	def __init__(self):
		# Imports and Variables
		import configparser as _configparser
		from .. import tui as _tui
		from .. import _MSG
		from .. import Classes as _Classes
		from .. import Path as _Path
		from .. import OS as _OS
		from .. import Lists as _Lists
		self.tui = _tui
		self.classes = _Classes
		self.os = _OS
		self.path = _Path
		self.msg = _MSG
		self.lists = _Lists
		self.parser = _configparser

def typed_property(name, type_check):
	"""
	Create a typed property with the specified name and type check. \n
	Valid types are: bool, float, int, str \n

	Args:
		name (str): The name of the property.
		type_check (type): The type to check against.

	Returns:
		property: The created property.
	"""
	def getter(self):
		return getattr(self, name)

	def setter(self, new_val):
		if type_check == "bool":
			msg = _MSG.cl_log_err_must_bool
		elif type_check == "str":
			msg = _MSG.cl_log_err_must_str
		elif type_check == "int":
			msg = _MSG.cl_log_err_must_int
		elif type_check == "float":
			msg = _MSG.cl_log_err_must_float
		else:
			msg = f"Invalid type_check ({type_check}) for name ({name})."
			raise ValueError(msg)
		# Now, is the value actualy the proper type?
		if not isinstance(new_val, type_check):
			#self.WARNING(msg)
			raise ValueError(msg)
		setattr(self, name, new_val)
	
	# Function return
	return property(getter, setter)


