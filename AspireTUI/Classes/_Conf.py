"""
Description:
		Class: Conf
Usage:
		from AspireTUI.Classes import Conf
		myConf = Conf(filename, LOGFILE=log_filename, bVerbose=True)
		myConf.SectionName.Variable
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
#################################################################################################################
#####                                           Class: Conf                                                 #####
#################################################################################################################

# Main Section
class Conf:
	def __init__(self, 
			filename: str, 
			filename_config=None, 
			encoding="UTF-8", 
			bVerbose=False,  
			bDual=False, 
			LOGFILE=None
			):
		"""
			Handling configuration files with ease!
			Opimized for IDE supporting dynamic dot notations.
			
			Upon creation you can toggle some behaviour of the class.
			bVerbose:	Will show user & developer and 'os' actions.
			LOGFILE:	Writes and shows according to default settings
			LOG_CONFIG:	

			While accessing an instanced class like this:
			conf.settings.filename				# Returns filename
			conf.settings.filename = "NewName"	# Provides the filename used with this config (rename)
			conf.reload(bVerbose=True)			# Overwriting class creation setting and
			 									# 	reloading conf.filename, ignoring changes, informing user
			conf.reload(bSave=True)				# Save changes now, wait 3 seconds, then re-reads conf.filename
			conf.save()							# Saves current configuration as conf.filename
			conf.save("new.cfg")				# Exports current config to "new.cfg"
			conf.ig.							# Will expand the content of the current configuration

			At any given section or item you can (depending on context):
			conf.ig.add_section("New Section Name")
			conf.ig.New_Section_Name.add_key("bSomeBool")
			conf.ig.New_Section_Name.bSomeBool = False
			
		"""
		# Structure data in subsection
		def _SubSettings(self):	# , filename=filename, encoding=encoding, bVerbose=bVerbose, bDual=bDual, LOGFILE=LOGFILE
			self.filename = filename
			self.encoding = encoding
			self.bVerbose = bVerbose
			self.bDual = bDual
			self.LOGFILE = LOGFILE
		# Prepare settings
		self.settings = _SubSettings()
		#self.settings.filename = filename
		#self.settings.encoding = encoding
		#self.settings.bVerbose = bVerbose
		#self.settings.bDual = bDual
		#self.settings.LOGFILE = LOGFILE
		#self.settings.
		# Imports and Variables
		import configparser as _configparser
		from AspireTUI import tui as _tui
		from AspireTUI import _MSG
		from AspireTUI import Classes as _Classes
		from AspireTUI import path as _uf
		import AspireTUI.Lists as _Lists
		self._tui = _tui
		self._msg = _MSG
		_known_extensions = {"ini", "cfg", "conf"}

		if LOGFILE:
			ret, log = _Classes.Log( LOGFILE , bVerbose=bVerbose, bDual=True)
			
			if _tui.status(ret, f"{self._msg.word_filesystem_file}"):
				# TODO
				pass
				
			if LOGFILE:
				if _uf.file_exists(LOGFILE, bVerbose=bVerbose):
					if LOGFILE.__getattribute__("Name"):
						self._logfile = _Classes.Log(LOGFILE)
				if LOG_CONFIG:
					self._logfile.settings.load(LOG_CONFIG)
		else:
			# Is empty
			self._logfile = LOGFILE
		self.bVerbose = bVerbose
		self._config = _configparser.ConfigParser()
		
	def _if_Verbose(self, msg: str):
		"""
			
		"""
		if self.settings.bVerbose:
			self._tui.status(True, "Is Verbose")
		elif self.settings.LOGFILE:
			self._tui.status(True, "Is a logfile")
			self._logfile.status()
		else:
			self._tui.status(False)
	
	def _read(self):
		# Prepare message
		tmp_msg = f"{self._msg.cl_conf_ui_reading}: {self.settings.filename}"
		# Prefer LOG over verbose
		if self.settings.LOGFILE:
			self._logfile.INFO(tmp_msg)
		elif self.settings.bVerbose:
			# Fallback to 
			self._tui.status(_Lists.StatusEnum.Work.id, tmp_msg)
		# Do it
		if self._config.read(self.filename, encoding=self.encoding):
			ret = True
		else:
			ret = False
		# Job is done, report...?
		# Prefer LOG over verbose... again!
		tmp_msg = f"{self._msg.cl_conf_ui_read}: {self.settings.filename}"
		if self.settings.LOGFILE:
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
		_read()

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

	class _Section:
		def __init__(self, conf, section):
			self.conf = conf
			self.section = section

		def __getattr__(self, key):
			if key not in self.conf._get_section(self.section):
				self.conf._add_key(self.section, key, "")
			return _Key(self, key)
	
	@property
	def _sections(self):
		return list(self._config.sections())

	def __getattr__(self, section):
		if section not in self._config:
			self._add_section(section)
		return _Section(self, section)

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
	
