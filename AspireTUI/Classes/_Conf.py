"""
Description:
		Class: Conf

Usage:
		from AspireTUI.Classes import Conf
		# Option A
		# - Runtime-Only-Config:
		myConf = Conf()

		# Option B
		# - Using the Conf class from multiple modules (ATTENTION: bAutoSafe and bAutoLoad will increase disk usage DRASTICLY!):
		myConf = Conf("myApp.ini", LOG="myApp.log", bVerbose=True, bAutoSafe=True, bAutoLoad=True)

		# Either way:
		myConf.ig.Section.Key = Value
		myConf.ig.Defaults.ImageExport = "jpg"
		# Or show value to user:
		tui.print("Default Image Export", myConf.ig.Defaults.ImageExport)

Notes:
		If a LOG_CONFIG= is passed and the file exists, it will be read.
		If it does not exist, the default/passed settings will be written into LOG_CONFIG
		See: myLog.settings for details.
========================================================
Created on:		2024 Jan. 08
Created by:		Simon Arjuna Erat
License:		MIT
URL:			https://www.github.com/sri-arjuna/ASPIRE

Based on my TUI & SWARM for the BASH shell © 2011
"""
from .._MESSAGES import current as _MSG
#
#	NEW
#
def typed_property(name, type_check):
	"""
	Create a typed property with the specified name and type check.

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

	return property(getter, setter)


## TODO: to be shared in .Classes
class _SectionSettings:
	def __init__(self):
		"""
		Provides basic settings for LOG and CONF classes 	\n
		Values need to be set from its parent class.
		"""
		class _subLog(self):
			# Contains values related to logs
			self.file = ""
			self.conf = ""
			self.level_show_user = 3
			self.level_save_log = 4
		class _subConf(self):
			# Contains values related to conf - config
			self.filename = ""
			self.sections = "[]"
			self.value_sep = " = "
			self.encoding = "UTF-8"
		# Namne of the actual conf or log file
		self.conf = _subConf(self)
		self.log = _subLog(self)
		self.bVerbose = False
		



#################################################################################################################
#####                                           Class: Conf                                                 #####
#################################################################################################################

# Main Section
class Conf:
	def __init__(self, 
			filename: str=None, 
			LOG: str=None, 
			filename_config=None, 
			encoding="UTF-8", 
			bVerbose=False,  
			bDual=False, 
			bAutoSafe=False,
			bAutoLoad=False
			):
		"""
			Handling configuration files with ease!
			Opimized for IDE supporting dynamic dot notations.
			
			Upon creation you can toggle some behaviour of the class.
			bVerbose:	Will show user & developer and 'os' actions.
			LOG:	Writes and shows according to default settings
			LOG_CONFIG:	Conf file that contains the configuration for the logfile.

			While accessing an instanced class like this:
			conf.settings.filename				# Returns filename
			conf.settings.filename = "NewName"	# Provides the filename used with this config (rename)
			conf.reload(bVerbose=True)			# Overwriting class creation setting and
			 									# 	reloading conf.filename, ignoring changes, informing user
			conf.reload(bSave=True)				# Save changes now, then re-reads conf.filename
			conf.save()							# Saves current configuration as conf.filename
			conf.save("new.cfg")				# Exports current config to "new.cfg"
			conf.ig.							# Will expand the content of the current configuration

			At any given section or item you can (depending on context):
			conf.ig.add_section("New Section Name")
			conf.ig.New_Section_Name.add_key("bSomeBool")
			conf.ig.New_Section_Name.bSomeBool = False
			
		"""
		# Prepare tools
		class _SectionTools(self):
			self.tui = ""
			self.msg = ""
			self.lists = ""
			self.parser = ""
		# Prepare settings
		self.settings = _SectionSettings(self)
		# Imports and Variables
		import configparser as _configparser
		from .. import tui as _tui
		from .. import _MSG
		from .. import Classes as _Classes
		from .. import Path as _Path
		from .. import Lists as _Lists
		self._tools = _SectionTools(self)
		self._tools.tui = _tui
		self._tools.msg = _MSG
		self._tools.lists = _Lists
		self._tools.parser = _configparser
		self.ig = self._prepare_sections()
		_known_extensions = {"ini", "cfg", "conf"}

		def _prepare_sections(self):
			# Helper method to dynamically create attributes for each section
			#sections = self._config.sections()
			sections = self._tools.parser.sections()
			ig_attribute = type("ig", (), {section: self._create_section(section) for section in sections})
			return ig_attribute
		def _create_section(self, section):
			# Helper method to dynamically create attributes for keys within a section
			class Section:
				def __getattr__(self, key):
					return self._tools.parser.get(section, key)
			return Section()
		

		if LOG:
			ret, log = _Classes.Log( LOG , bVerbose=bVerbose, bDual=True)
			
			if _tui.status(ret, f"{self._msg.word_filesystem_file}"):
				# TODO
				pass
				
			if LOG:
				if _Path.file_exists(LOG, bVerbose=bVerbose):
					if LOG.__getattribute__("Name"):
						self._logfile = _Classes.Log(LOG)
		else:
			# Is empty
			self._logfile = LOG
		self.bVerbose = bVerbose
		self._config = _configparser.ConfigParser()
		
	def _if_Verbose(self, msg: str):
		"""
			
		"""
		if self.settings.bVerbose:
			self._tui.status(True, "Is Verbose")
		elif self.settings.LOG:
			self._tui.status(True, "Is a logfile")
			self._logfile.status()
		else:
			self._tui.status(False)
	
	def _read(self):
		# Prepare message
		tmp_msg = f"{self._msg.cl_conf_ui_reading}: {self.settings.filename}"
		# Prefer LOG over verbose
		if self.settings.LOG:
			self._logfile.INFO(tmp_msg)
		elif self.settings.bVerbose:
			# Fallback to 
			self._tui.status(self._lists.StatusEnum.Work.id, tmp_msg)
		# Do it
		if self._config.read(self.filename, encoding=self.encoding):
			ret = True
		else:
			ret = False
		# Job is done, report...?
		# Prefer LOG over verbose... again!
		tmp_msg = f"{self._msg.cl_conf_ui_read}: {self.settings.filename}"
		if self.settings.LOG:
			if ret:
				self._logfile.INFO(tmp_msg)
			else:
				self._logfile.WARNING(tmp_msg)
		elif self.settings.bVerbose:
			# Fallback to 
			self._tui.status(ret, tmp_msg)
		
	def _save(self, filename:str):
		with open(self.filename, 'w', encoding=self.encoding) as _configfile:
			self._config.write(_configfile)

	def _reload(self):
		self._read(self)

	def _add_section(self, section):
		self._config.add_section(section)
		self._save()

	def _rename_section(self, old_name, new_name):
		self._config[new_name] = self._config[old_name]
		del self._config[old_name]
		self._save()

	def _add_key(self, section, key, value):
		self._config.set(section, key, value)
		self._save()

	def _remove_key(self, section, key):
		self._config.remove_option(section, key)
		self._save()

	def _rename_key(self, section, old_key, new_key):
		value = self._config[section].pop(old_key)
		self._config[section][new_key] = value
		self._save()

	def _get_section(self, section):
		return self._config[section]

	def _get_key(self, section, key):
		return self._config.get(section, key)

	def _set_key(self, section, key, value):
		self._config.set(section, key, value)
		self._save()

	def reload(self):
		self._reload()

	def save(self):
		self._save()

	class _Key:
		def __init__(self, section, key):
			self.section = section
			self.key = key
		@property
		def value(self):
			return self.section.conf._get_key(self.section.section, self.key)
		@value.setter
		def value(self, new_value):
			self.section.conf._set_key(self.section.section, self.key, new_value)
		def rename(self, new_name):
			self.section.conf._rename_key(self.section.section, self.key, new_name)
			return self.section.conf.__getattr__(self.section.section).__getattr__(new_name)
		def remove(self):
			self.section.conf._remove_key(self.section.section, self.key)
			
	class _Section:
		def __init__(self, conf, section):
			self.conf = conf
			self.section = section

		def __getattr__(self, key):
			if key not in self.conf._get_section(self.section):
				self.conf._add_key(self.section, key, "")
			return self.conf._Key(self, key)
	
		@property
		def _sections(self):
			return list(self._config.sections())

		def __getattr__(self, section):
			if section not in self._config:
				self._add_section(section)
			return self.conf._Section(self, section)
