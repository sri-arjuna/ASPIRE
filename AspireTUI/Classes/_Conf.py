"""
Description:\n
		Class: Conf

Usage:\n
		from AspireTUI.Classes import Conf

Examples:\n
		\# Ideal for "forced" settings, that still can be adjusted\n

			myConf = Conf()

		
		\# Full fledged call 

		\# (ATTENTION: bAutoSafe and bAutoLoad will increase disk usage DRASTICLY!):

			myConf = Conf("myApp.ini", LOG="myApp.log", bVerbose=True, bAutoSafe=True, bAutoLoad=True)

		
		\# Either way:

			myConf.ig.Section.Key = Value          # Syntax

			myConf.ig.Defaults.ImageExport = "jpg" # Example

		\# Or show value to user:

			tui.print("Default Image Export", myConf.ig.Defaults.ImageExport)

		
Notes:

		If a LOG_CONFIG= is passed and the file exists, it will be read.

		If it does not exist, the default/passed settings will be written into LOG_CONFIG

		See: myLog.settings for details.


========================================================

Created on:		2024 Jan. 08

Created by:		Simon Arjuna Erat

License:		MIT

URL:			https://www.github.com/sri-arjuna/AspireTUI

Based on my TUI & SWARM for the BASH shell © 2011
"""
#
#	Imports
#
from .._MESSAGES import current as _MSG
from ..Lists import LOG_LEVEL as LEVEL
from . import _shared

#################################################################################################################
#####                                           Class: Conf                                                 #####
#################################################################################################################
# Main Section
class Conf:
	def __init__(self, 
			filename: str=None,
			log: str=None,
			name: str=None,
			comment: str=None,
			bVerbose: bool=False,
			bAutoSave: bool=False,
			bAutoLoad: bool=False,
			iShowUser: int=2,
			iSaveLog: int=0,
			encoding: str="UTF-8",
			format: str="%H:%M:%S.%f"
			):
		"""
Handling configuration files with ease!

Opimized for IDE supporting dynamic dot notations.


Upon creation you can toggle some behaviour of the class.

  bVerbose:	Will show user & developer and 'os' actions.
  
  LOG:		Writes and shows according to default settings
  
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
		#
		#	Get sub menus
		#
		# Actual initialize class
		from . import _shared
		#import configparser
		self.tools = _shared.SectionTools()
		self.settings = _shared.SectionSettings()
		# Apply arguments
		self.settings.name = name
		self.settings.bAutoSave = bAutoSave
		self.settings.bVerbose = bVerbose
		self.settings.encoding = encoding
				
		# Set filename at the proper place
		self.settings.conf.file = filename
		if bVerbose:
			self.tools.tui.status(LEVEL.INFO.value, "Filename (ini):", filename)
		if log:
			self.settings.log.file = log
			if bVerbose:
				self.tools.tui.status(LEVEL.INFO.value, "Filename (log):", filename)
			LOG = self.tools.classes.Log(log, bVerbose, bAutoSave , iSaveLog, iShowUser, name, comment, encoding, format)
		else:
			LOG = self.tools.classes.Log()
		#LOG.FATAL("Test entry")
		#print("---- Test entry -------")
		# Back up first parser
		# self.settings.conf.file = "myConf.ini"
		#LOG.DEBUG(f"conf-init: self.settings.conf.file == {self.settings.conf.file}")
		# Prepare handlers
		
		if self.settings.conf.file:
			# Config file value is set
			LOG.DEBUG("conf-init: Filename string valid, open for parsing")
			self._config = self.tools.parser.ConfigParser()
			self._config.read(self.settings.conf.file ) #, self.settings.encoding)
		
		#dir_logs = self._config['CLASSE']['DIR_LOGS']
		#print("DIR_LOGS:", dir_logs)
		#return
		"""
		def _prepare_sections(self, cls):
			# Helper method to dynamically create attributes for each section
			#sections = self._config.sections()
			sections = cls._config.sections()
			ig_attribute = type("ig", (), {section: _create_section(section) for section in sections})
			return ig_attribute
		def _create_section(self, cls, section):
			# Helper method to dynamically create attributes for keys within a section
			class Section:
				def __getattr__(self, cls, key):
					return cls._config.get(section, key)
			return Section()

		#self._prepare_sections = _prepare_sections
		#self.ig = _shared._prepare_sections(self) #   _prepare_sections(self) 
		self.ig = _prepare_sections(self, cls=self)
		"""		
	
	def _if_Verbose(self, msg: str):
		"""
			
		"""
		if self.settings.bVerbose:
			self.tools.tui.status(True, "Is Verbose")
		elif self.settings.LOG:
			self.tools.tui.status(True, "Is a logfile")
			self._logfile.status()
		else:
			self.tools.tui.status(False)
	
	def _read(self):
		# Prepare message
		tmp_msg = f"{self._msg.cl_conf_ui_reading}: {self.settings.filename}"
		# Prefer LOG over verbose
		if self.settings.LOG:
			self._logfile.INFO(tmp_msg)
		elif self.settings.bVerbose:
			# Fallback to 
			self.tools.tui.status(self.tools.lists.StatusEnum.Work.id, tmp_msg)
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
