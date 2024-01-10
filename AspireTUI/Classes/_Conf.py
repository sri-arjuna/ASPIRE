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
class Conf:
	def __init__(self, filename: str, encoding="UTF-8", bVerbose=False, LOGFILE=None, LOG_CONFIG=None):
		import configparser as _configparser
		from AspireTUI import tui as _tui
		from AspireTUI._MESSAGES import english as _msg
		from AspireTUI import Classes as _Classes
		from AspireTUI import UtilsFile as _uf
		
		self._tui = _tui
		self._msg = _msg
		self.filename = filename
		self.encoding = encoding
		if LOGFILE:
			if _uf.
			self._logfile = _Classes.Log(LOGFILE)
			if LOG_CONFIG:
				self._logfile.config.load(LOG_CONFIG)
		else:
			# Is empty
			self._logfile = LOGFILE
		self._bVerbose = bVerbose
		self._config = _configparser.ConfigParser()
		
		
	def _read(self)):
		if self._bVerbose:
			self._tui.status(4, self._msg.cl_conf_ui_reading)
		if self._logfile is not None:

		self._config.read(self.filename, encoding=self.encoding,)
	
	def _save(self):
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

	@property
	def sections(self):
		return list(self._config.sections())

	def __getattr__(self, section):
		if section not in self._config:
			self._add_section(section)
		return Section(self, section)

	class Section:
	def __init__(self, conf, section):
		self.conf = conf
		self.section = section

	def __getattr__(self, key):
		if key not in self.conf._get_section(self.section):
			self.conf._add_key(self.section, key, "")
		return Key(self, key)

	class Key:
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
