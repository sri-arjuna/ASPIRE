"""
# Application Manager

*most simple handling for cfg and log files*

from AspireTUI import Application

myApp = Application.Manager("MyApp")

myApp.DEBUG("Log level based output")

value = myApp.get("Section", "Key")

from AspireTUI import tui
tui._Theme.set("Tron")
tui.header()
tui.title("new conf")
-------------------------
CLASSIC.{get|set}(section,key[,val])
CLASSIC.DEBUG("")
CLASSIC.save()

"""
# Imports
import traceback
from .. import tui as _tui
from .. import Path as _Path
from .. import Strings as _stew
from .. import _VersionInfo
from ..Lists import LOG_LEVEL as LEVEL
from ..Lists import LOG_SEVERITY as SEVERITY
from .. import _settings_console as settings
#
#	Defaults
#
class AppManager:
	def __init__(self, 
			base_filename: str=None,
			base_section: str=None,
			bDefaultComment: bool=True,
			bAutoRead: bool=True,
			bAutoSave: bool=True,
			comment_conf: str=None,
			comment_log: str=None,
			bVerbose: bool=False,
			bDaily: bool=False,
			bDisableLog: bool=False,
			bDisableConf: bool=False,
			iShowUser: int=2,
			iSaveLog: int=1,
			encoding: str="UTF-8",
			log_format: str="%F %H:%M:%S.%f",
			ext_log: str="log",
			ext_conf: str="cfg",
			#chr_sep: str="=",
			#chr_sect: str="[]",
			#chr_comm: list=["#", ";"],
			theme: str="Default",
			theme_color: str=None,
			theme_style: str=None,
			#status_separators: str="[]"
			):
		"""# AppManager

*Handle conf-/logfiles and theme for your application*

Please note that:
* All your App settings can be accessed by simply using: get(key) or set(key, value)
* Theme & Log sections are supposed to be handled internaly only (or by {g/s}et_custom(section, key{, value]}))


# Usage:

from AspireTui.Classes import AppManager

#Minimal\n
myAppName = App("myAppName")

#With a non-default theme\n
myAppName = App("myAppName", theme="Elegance")

#This will read section "MyAppName" and return the value of key "thisKey"\n
myKeyValue = myAppName.get("thisKey")

#This will read section "CustomSection" and return the value of key "Something"\n
myCustomValue = myAppName.get_custom("CustomSection", "Something")



# Options - Class

base_filename: str	= This is used as the base filename for the config- and log file, as well as the main section for/of your own application settings

base_section: str	= This can be used to differ between different instances (for example, with different tasks) of AppManager that write to the same logfile

bDefaultComment: bool	= Set to 'False' to not write any comment heading (comment_conf & comment_log will overwrite this setting)

bForceRead: bool	= set to 'True' to force reading settings from the file every time, rather than from memory

bForceWrite: bool	= Set to 'False' to only apply settings to memory



# Options - Config

*If you want allow your users to change the theme, bDisableConf must be 'False'*

bDisableConf: bool	= Set to 'True' to not use/write a config file, this will "hardcode" to use settings used upon "instancing" AppManager

ext_conf: str	= Change this if you want another extension than "cfg" for your configfile

comment_conf: str	= Set a custom heading comment, supports strings with "\n" and lists. Overwrites 'bDefaultComment'



# Options - Log

bDisableLog: bool	= Set to 'True' to not use/write a log file

ext_log: str	= Change this if you want another extension than "log" for your logfile

comment_log: str	= Set a custom heading comment, supports strings with "\n" and lists. Overwrites 'bDefaultComment'

bDaily: bool	= Set to 'True' to create a new log file for each day

iSaveLog: int	= Set to 0-5 to only save error levels of that int or higher

iShowUser: int	= Set to 0-5 to only show messages of that error level or higher

encoding: str	= Replace 'UTF-8' with any valid encoding format

format: datetime	= Set to a 'datetime-format' to be used to prefix written log messages in the logfile
"""
		#
		#	Sub Menu - __Self
		#
		class DataContainer:
			def __init__(self):
				self = []

			def set(self, sector, key, value):
				for entry in self._values:
					if entry['sector'] == sector and entry['key'] == key:
						entry['value'] = value
						return
				# If not found, add a new entry
				self.append({'sector': sector, 'key': key, 'value': value})

			def get_value(self, sector, key):
				for entry in self:
					if entry['sector'] == sector and entry['key'] == key:
						return entry['value']
				return None
		class sub_self:
			def __init__(self, 
					base_filename: str=None,			# Used for: base_filename.{cfg|log}
					base_section: str=None,				# Useful if you have multiple modules (*.py)
					bDefaultComment: bool=True,			# Use default heading comment
					bAutoRead: bool=True,
					bAutoSave: bool=True,
					comment_conf: str=None,				# Force custom comment
					comment_log: str=None,				# Supports string with \n and lists
					bVerbose: bool=False,
					bDaily: bool=False,
					bDisableLog: bool=False,
					bDisableConf: bool=False,		## NEW TODO
					iShowUser: int=2,
					iSaveLog: int=0,
					encoding: str="UTF-8",
					log_format: str='%F %H:%M:%S.%f',
					ext_conf: str="cfg",
					ext_log: str="log",
					#chr_sep: str="=",
					#chr_sect: str="[]",
					#chr_comm: list=["#", ";"],
					theme: str="Default",
					theme_color: str=None,
					theme_style: str=None,
					#status_separators: str="[]"
					):
				self.base_filename = base_filename
				self.base_section = base_section
				self.bDefaultComment = bDefaultComment
				self.bAutoRead = bAutoRead
				self.bAutoSave = bAutoSave
				self.comment_conf = comment_conf
				self.comment_log = comment_log
				self.bVerbose = bVerbose
				self.bDaily = bDaily
				self.bDisableLog = bDisableLog
				self.bDisableConf = bDisableConf
				self.iShowUser = iShowUser
				self.iSaveLog = iSaveLog
				self.encoding = encoding
				self.log_format = log_format
				self.ext_conf = ext_conf
				self.ext_log = ext_log
				#self.chr_sep = chr_sep
				#self.chr_sect = chr_sect
				#self.chr_comm = chr_comm
				self.theme = theme
				self.theme_color = theme_color
				self.theme_style = theme_style
				#self.status_separators = status_separators
		# Assign values to class
		self._self = sub_self(
			base_filename=base_filename,
			base_section = base_section,
			bDefaultComment = bDefaultComment,
			bAutoRead = bAutoRead,
			bAutoSave = bAutoSave,
			comment_conf = comment_conf,
			comment_log = comment_log,
			bVerbose = bVerbose,
			bDaily = bDaily,
			bDisableLog = bDisableLog,
			bDisableConf = bDisableConf,
			iShowUser = iShowUser,
			iSaveLog = iSaveLog,
			encoding = encoding,
			log_format = log_format,
			ext_conf = ext_conf,
			ext_log = ext_log,
			#chr_sep = chr_sep,
			#chr_sect = chr_sect,
			#chr_comm = chr_comm,
			theme = theme,
			theme_color = theme_color,
			theme_style = theme_style,
			#status_separators = status_separators
		)
		###############################################################################################################
		####                                                 INIT                                                  ####
		###############################################################################################################
		import configparser as _cfgp
		from .. import Path as _Path
		from .. import OS as _OS
		self.tui = _tui
		#print(f"Initialized: {self._self.bDisableConf}, Type: {type(self._self.bDisableConf)}")
		# Apply theme
		if self._self.theme == "Custom":
			self.tui._Theme.set(self._self.theme, theme_style=theme_style, theme_color=theme_color)
		else:
			self.tui._Theme.set(self._self.theme)
		
		# Assign Aspire functions to class for easy use
		self.Path = _Path
		self.OS = _OS
		
		# Data Container
		self.messages = []
		self._content = []
		self._sections = []
		self._keys = []
		self._values = []
		
		# Verify base_filename
		if "/" in base_filename or "\\" in base_filename:
			# Has a regular path:
			self._file_dir = _tui._os.path.abspath(base_filename).replace("\\","/")
		else:
			# No path provided, use current dir (usualy where the script/bin is)
			self._file_dir = _tui._os.path.abspath(base_filename).replace("\\","/")
		# Adjust dir to not have basefilename
		self._file_dir = self._file_dir.replace(base_filename,"")
		
		# Create filenames from passed base_filename
		self._file_conf = f"{self._file_dir}/{self.__get_name_conf()}"
		self._file_log = f"{self._file_dir}/{self.__get_name_log()}"
		#print("DEUG INIT: ", self._file_dir)
		
		# Is it a daily log?
		if self._self.bDaily:
			if not _Path.exists(self._file_log):
				# Create logfile if it does not exist
				self.__create_log()
		
		# Read config file data
		self.read()

	###############################################################################################################
	####                                       Internal Tools                                                  ####
	###############################################################################################################
	def __get_name_log(self):
		"""
		Returns the generated log name, or None
		"""
		if self._self.base_filename:
			# Prepare varnames
			n = self._self.base_filename
			l = self._self.ext_log
			t = _stew.date().replace(".","_")
			
			# Adjust for daily log
			if self._self.bDaily:
				return f"{n}-{t}.{l}"
			else:
				return f"{n}.{l}"
		else:
			# No filename passed
			return None
	
	def __get_name_conf(self):
		"""
		Returns the generated conf name, or None
		"""
		if self._self.base_filename:
			return f"{self._self.base_filename}.{self._self.ext_conf}"
		else:
			return None
		
	def __write_log(cls, level, *args):
		"""
		Write the actual log entries
		"""
		err_msg = "To log a message, you must pass a level (int) and a message (str)."
		# Verify passed arguments
		if level is None or args is None:
			# No values passed, abort
			_tui.status(False, err_msg)
			return False
		# Prepare message from *args
		if isinstance(args[0], int):
			#if level == args[1]
			level = args[0]
			args_new = args[1:]
		else:
			args_new = args

		if len(args_new) == 1:
			message = args_new[0]
		else:
			msg_str = args_new[0]
			try:
				message = msg_str % args_new[1:]
			except:
				message = msg_str
				for a in args:
					message = f"{message} {a}"
		
		# Prepare DateTime string
		current_time = _stew._datetime.now()
		formatted_time = current_time.strftime(cls._self.log_format)	#  . strftime // strptime
		
		# Final actions
		global SEVERITY
		iSaveLog = int(cls._self.iSaveLog)
		iShowUser = int(cls._self.iShowUser) 
		if level >= iShowUser: # - 1:
			num = 1000 + level
			#print("DEBUG: ", num, message)
			for stat in _tui._put.STATUS: #.__reversed__():
				if num in stat.value:
					break
				if num == stat.value.id:
					#_tui.status(num, f"DEBUG stat.value.id == {num}")
					break
			ret = _tui.status(stat.value, message)
			#cls.DEBUG(f"DEBUG: {stat.value}")
		if level >= iSaveLog: # <= : # - 1:
			# Prepare output
			n = SEVERITY[level]
			if len(n) <= 6:
				n = f"{n}\t"
			output = f"{formatted_time} {level}-{n}"
			if cls._self.base_section:
				tmp = cls._self.base_section
				if len(tmp) <= 8:
					tmp = f"{tmp}\t"
				output = f"{output}\t{tmp}"
			output = f"{output}\t{message}"
			# Write to log
			if bool(cls._self.bDisableLog): # or not cls._self.base_filename:
				cls.messages.append(output)
			else:
				fn = cls.__get_name_log()
				#print(f"Should write: {output} --> {fn}")
				# Verify we have a filename or section name
				if fn:
					with open(fn, 'a' , encoding=cls._self.encoding) as thisLOG:
						print(f"{output}", file=thisLOG)
	
	def list_sections(cls) -> list:
		"""
		Returns a list of sections
		"""
		out = []
		for sec in cls._sections:
			if not sec in out:
				out.append(sec)
		return out
	
	def list_keys(cls, Section:str=None) -> list:
		"""
		Returns list of all keys from Section
		"""
		if not Section:
			ValueError(Section)
		out = []
		C=0
		MAX = len(cls._sections)

		while C < MAX:
			if cls._sections[C] == Section:
				if not cls._keys[C] in out:
					out.append(cls._keys[C])
			C+=1
		return out
	###############################################################################################################
	####                                       First time use                                                  ####
	###############################################################################################################
	def __create_log(self):
		"""
		Writes the heading comment of the logfile.

		If bDisableLog = True, the heading comment is appended to messages.

		If / When you use myAppName.save(), a logfile will be created anyway.
		"""
		# Init default values
		message: str=None
		ret_bool = False
		logfile = None
		logfile = self.__get_name_log()
		hasHeader=False

		# Keep in memory?
		if self._self.bDisableLog or logfile is None:
			# Write to self.message
			for msg in message.split("\n"):
				self.messages.append(f"# {msg}")
			# All done
			return True
		
		# No, actualy write a file
		# Check if file exists
		if _Path.isFile(logfile):
			# File exists, check for log header comment
			with open(logfile, "r", encoding=self._self.encoding) as fn:
				# Read the first line
				first_line = fn.readline()
				# Check if it starts with '#'
				if first_line.startswith("#"):
					hasHeader = True
		else:
			# File does not exist, write heading for sure
			hasHeader=False
		
		# Write header if missing
		if not hasHeader:
			# Prepare header:
			if self._self.comment_log is not None:
				# Custom heading is passed, use that
				message = self._self.comment_log
			else:
				# Use default heading:
				message = f"{_VersionInfo.FileGenComment}\n"
				message += f"Logfile created for '{self._self.base_filename}' on {_stew.now()}"
				message += f"\nDatetime                 Level        Type        Message"
			
			# Write message
			with open(logfile, "a", encoding=self._self.encoding) as fn:
				for msg in message.split("\n"):
					print(f"# {msg}", file=fn)
				ret_bool = True
		# All done
		return ret_bool
	
	def __create_conf(self):
		"""
		Writes the heading comment of the configuration file.

		Skip this function if no conf file is used
		"""
		message: str=None
		if self._self.bDefaultComment:
			message = f"{_VersionInfo.FileGenComment}\n"
			message += f"Conffile created for '{self._self.base_filename}' on {_stew.now()}"
		if self._self.comment_conf:
			# Its not none, overwriting default message
			message = self._self.comment_conf
		# Actually write the conf file
		with open(self.__get_name_conf(),"a",encoding=self._self.encoding) as fn:
			#
			#	Write the heading
			# 
			for msg in message.split("\n"):
				print(f"# {msg}", file=fn)
			#
			# 	Create default entries:
			#
			cfg_defaults = ""
			cfg_defaults += f""
			cfg_defaults += f"[Log]\n"
			cfg_defaults += f"iSaveLog={self._self.iSaveLog}\n"
			cfg_defaults += f"iShowUser={self._self.iShowUser}\n"
			cfg_defaults += f"bDaily={self._self.bDaily}\n"
			cfg_defaults += f"encoding={self._self.encoding}\n"
			cfg_defaults += f"format=\"{self._self.log_format}\"\n"
			
			# Prepare theme variales
			tmp_list = "" #_tui._Theme.list()
			tmp_colors = "" #_tui._Theme.list_color()
			for tt in _tui._Theme.list():
				tmp_list += f", {tt}"
			for tc in _tui._Theme.list_color():
				tmp_colors += f", {tc}"
			# Add theme related values
			cfg_defaults += f"\n"
			cfg_defaults += f"# THEME can be set to 'Custom', use the following according values to change the appearance of {self._self.base_filename}\n"
			cfg_defaults += f"# Theme/-Style options: {tmp_list[2:]}\n"
			cfg_defaults += f"# Theme-Color options:  {tmp_colors[2:]}\n"
			cfg_defaults += f"# THEME_COLOR and THEME_STYLE are only read/used when THEME=Custom\n"
			cfg_defaults += f"[Theme]\n"
			cfg_defaults += f"THEME={self._self.theme}\n"
			cfg_defaults += f"THEME_COLOR={self._self.theme_color}\n"
			cfg_defaults += f"THEME_STYLE={self._self.theme_style}\n"
			#
			#	Write default entries
			#
			for cfg in cfg_defaults.split("\n"):
				print(f"{cfg}", file=fn)
	
	###############################################################################################################
	####                                      Log functions                                                    ####
	###############################################################################################################
	def DEBUG(cls, *args):
		""""
		Show / Save message to user / file
		"""
		cls.__write_log(0, *args)
	def INFO(cls, *args):
		""""
		Show / Save message to user / file
		"""
		cls.__write_log(1, *args)
	def WARNING(cls, *args):
		""""
		Show / Save message to user / file
		"""
		cls.__write_log(2, *args)
	def ERROR(cls, *args):
		""""
		Show / Save message to user / file
		"""
		cls.__write_log(3, *args)
	def CRITICAL(cls, *args):
		""""
		Show / Save message to user / file
		"""
		cls.__write_log(4, *args)
	def FATAL(cls, *args):
		""""
		Show / Save message to user / file
		"""
		cls.__write_log(5, *args)
	
		###############################################################################################################
	####                                  Conf functions - get() & set()                                       ####
	###############################################################################################################
	def get(cls, Key: str=None):
		"""
		Returns the value of your setting

		This is a wrapper for: get_custom(base_filename, Key)
		"""
		retval = None
		retval = cls.get_custom(cls._self.base_filename, Key)
		return retval
	
	def set(cls, Key: str=None, Value=None) -> bool:
		"""
		Returns the value of your setting

		This is a wrapper for: get_custom(base_filename, Key)
		"""
		return cls.set_custom(cls._self.base_filename, Key, Value)
	
	def get_custom(cls, Section: str=None, Key: str=None, bVerbose=False):
		"""
		Raturns the value from the 'key=' of '[section]'
		"""
		if Section in cls.list_sections() and Key in cls.list_keys(Section):
			pass
		elif Section is None or Key is None:
			msg = f"'AppMAnager.get_custom()': {_tui._MSG.args_missing} / sec:{Section} / key:{Key}"
			cls.ERROR(msg)
			return False
		C=0
		cls.read()
		MAX = len(cls._sections)
		out = None
		while C <= MAX:
			if cls._sections[C] == Section and cls._keys[C] == Key:
				out = cls._values[C]
				break
			C+=1
			if C == MAX: 
				break
		if out is None:
			_tui.status(False, "Could not retrieve Value for:", f"Section: {Section} / Key: {Key}")
			return None
		else:
			return out
	
	def set_custom(cls, Section: str=None, Key: str=None, Value: str=None, bVerbose=False) -> bool:
		"""
		Set the value for the'[section]' with 'key=value'
		"""
		ret_bool = False
		if Section is None or Key is None or Value is None:
			msg = f"'AppMAnager.set_custom()': {_tui._MSG.args_missing} / sec:{Section} / key:{Key} / var:{Value}"
			cls.FATAL(msg)
			return False
		
		# If not found, add a new entry
		if Key not in cls._keys:
			i = len(cls._keys)
			cls._sections.append(Section)
			cls._keys.append(Key)
			cls._values.append(Value)
			if bVerbose: 
				cls.DEBUG(f"cfg - Set: Added Key:{Key} in Section:{Section} with Value: {Value}")
			ret_bool = True
		else:
			# Update values
			C=0
			MAX = len(cls._sections)
			while C <= MAX:
				#print("DEBUG: set_custom: ", C, MAX, Section, Key, Value)
				if cls._sections[C] == Section and cls._keys[C] == Key:
					if {cls._values[C]} != Value:
						if bVerbose: 
							cls.DEBUG(f"cfg - Set: Update value from '{cls._values[C]}' to '{Value}' in '{Section}' '{Key}'")
						cls._values[C] = Value
						ret_bool = True
						break
				C+=1
		if not ret_bool:
			if bVerbose: print(f"set: why not set/update: {Section}, {Key}, {Value} -- Not an issue yet, but might be??")
		#
		# Instant save?
		#
		if cls._self.bAutoSave: 
			cls.save()
		if bVerbose: 
			_tui.status(ret_bool, f"{Key}={Value}")
		return ret_bool
	
	###############################################################################################################
	####                                 Conf functions - Read & Write                                         ####
	###############################################################################################################
	def read(cls):
		"""
		Reads the configuration file and applies internals (Log & Theme) and "this_App" settings.

		This is called automaticly as long:
		* bForceRead = True
		* bDisableLog = False OR bDisableConf=False
		"""
		#
		# Get file names
		#
		fn = cls.__get_name_conf()
		logfile = cls.__get_name_log()

		#
		# Reset data containers
		# 
		cls._content = []
		cls._values = []
		cls._keys = []
		cls._sections = []

		#
		#	Fill datacontainer with passed variables
		#	Overwrite later with values from config file
		#
		L = "Log"
		cls._sections.append(L) , cls._keys.append("iSaveLog") 	, cls._values.append(cls._self.iSaveLog)
		cls._sections.append(L) , cls._keys.append("iShowUser") , cls._values.append(cls._self.iShowUser)
		cls._sections.append(L) , cls._keys.append("bDaily") 	, cls._values.append(cls._self.bDaily)
		cls._sections.append(L) , cls._keys.append("encoding") 	, cls._values.append(cls._self.encoding)
		cls._sections.append(L) , cls._keys.append("format") 	, cls._values.append(cls._self.log_format)
		
		T = "Theme"
		cls._sections.append(T) , cls._keys.append("THEME") 		, cls._values.append(cls._self.theme)
		cls._sections.append(T) , cls._keys.append("THEME_COLOR") 	, cls._values.append(cls._self.theme_color)
		cls._sections.append(T) , cls._keys.append("THEME_STYLE") 	, cls._values.append(cls._self.theme_style)

		#
		# Wrap around configparser
		# No need to try reading (or create) a config file
		#
		if not cls._self.bDisableConf:# is False:
			# Only create conf file if Disable=False
			if not _Path.exists(fn): #, True):
				# No config file exists, write initial template:
				cls.__create_conf()
			# A conf file can only be read if it exists
			import configparser as _cfgp
			this_config = _cfgp.ConfigParser(interpolation=None)
			# Preserve CaseSensitify
			this_config.optionxform = str
			# Open file
			this_config.read(fn)
		
			#
			# Fill and Update Data containers
			#
			for section in this_config.sections():
				section_list = this_config.options(section)
				for key in section_list:
					# Get value for append or update
					val = this_config.get(section, key)
					# Check if internal (update) or append (from file)
					if section in "Theme, Log":
						# its an internal config, update it
						cu = 0 # ConfigUpdate
						while cu <= len(cls._keys):
							if section == cls._sections[cu] and key == cls._keys[cu]:
								# Update this
								cls._values[cu] = _stew.strip_quotes(val)
								#print("val: ", val)
								#print("_values: ", cls._values[cu])
								break
							cu += 1
					else:
						cls._sections.append(section)
						cls._keys.append(key)
						cls._values.append(_stew.strip_quotes(val))
		
		#
		# Wrap around log
		#
		if not cls._self.bDisableConf:
			if logfile:
				# Create logfile first - if required:
				if not _Path.exists(logfile):
					cls.__create_log()
					if cls._self.bVerbose: cls.DEBUG(f"cfg - Read: Created: {cls._file_log}")
		
		###########################################################################################################
		####                                    Theme handling                                                 ####
		###########################################################################################################
		#
		#	Make initial update of theme, expecting proper values
		#
		if True:
			cls._self.theme 		= this_config.get("Theme", "THEME")
			cls._self.theme_style	= this_config.get("Theme", "THEME_STYLE")
			cls._self.theme_color	= this_config.get("Theme", "THEME_COLOR")
			_tui._Theme.set(cls._self.theme, cls._self.theme_style, cls._self.theme_color)		
		
		# This is the update TUI according to config:
		_tui._settings["theme"] = cls._self.theme
		_tui._settings["theme_color"] = cls._self.theme_color
		_tui._settings["theme_style"] = cls._self.theme_style


		# Check for valid theme entry / value
		this_theme = cls._self.theme
		if this_theme is None : 
			this_theme = "Default"
			cls._self.theme = this_theme
		elif this_theme not in _tui._Theme.list() and this_theme.lower() != "random" and this_theme.lower() != "custom":
			this_theme = "Default"
			cls._self.theme = this_theme
		
		# Handle the theme
		lst_theme = list(_tui._Theme.list())
		
		#
		#	Special handling first
		#
		if "random" == str(this_theme).lower():
			# Check if random already had been applied
			if str(settings["theme"]).lower() == "random":
				import random
				rnd_theme = random.choice(lst_theme)
				cls._self.theme = rnd_theme
				# Apply theme that is neither "Default" nor literal "Random"
				settings["theme"] = rnd_theme
				_tui._Theme.set(cls._self.theme)
				cls.DEBUG(f"Theme applied (RANDOM): {cls._self.theme}")
		elif "custom" == str(this_theme).lower():
			# This should apply the custom color and style to the _settings
			#print("should apply custom")
			_tui._Theme.set("Custom", cls._self.theme_style, cls._self.theme_color)
			cls.DEBUG(f"Theme applied (CUSTOM): STYLE={cls._self.theme_style}, COLOR={cls._self.theme_color}")
			#_tui._Theme.get()
		else:
			#cls._self.theme = this_theme
			_tui._Theme.set(cls._self.theme)
			cls.DEBUG(f"Theme applied: {cls._self.theme}")
		
		# This _should_ update the theme according to what theme was set previously
		
		#cls.DEBUG(_tui._settings)
		#_tui._Theme.get()
		return True
	
	def save(cls):
		"""
		Saves data to conf file.

		If only data related to [AspireTUI] (log) is available, it skips writing the file.
		"""
		# Skip with success if bDisableConf AND bDisableLog are True.
		if cls._self.bDisableConf and cls._self.bDisableLog:
			return True
		
		#
		# Get file names
		#
		fn = cls._file_conf #cls.__get_name_conf()
		logfile = cls._file_log #cls.__get_name_log() # TODO: ?? cls._file_log

		#################################################################################
		#
		#	Lets handle them individualy --> LOG
		#
		#################################################################################
		if not cls._self.bDisableLog:
			# Logfile is enable
			if cls.messages and logfile:
				# Something is there
				if cls._self.bVerbose: cls.DEBUG(f"log - Save: Writing messages to: {cls._file_log}")
				with open(cls._file_log, "a", encoding=cls._self.encoding) as thisLOG:
					for entry in cls.messages: print(entry, file=thisLOG)
		
		#################################################################################
		#
		#	Lets handle them individualy --> Conf
		#
		#################################################################################
		if not cls._self.bDisableConf:
			#	Config file is enabled
			#	Private functions to handle/keep comments in ini file
			#
			def read_with_comments(filename):
				"""
				Reads a config file and retains comments.
				"""
				with open(filename, 'r', encoding='utf-8') as file:
					lines = file.readlines()

				config = _cfgp.ConfigParser(interpolation=None)
				config.optionxform = str  # Preserve case
				config.read(filename)

				return config, lines

			def write_with_comments(filename, config, lines):
				"""
				Writes a config file and preserves comments and the correct separator.
				"""
				section = None  # Initialize section outside of the loop
				val_sep = None

				with open(filename, 'w', encoding='utf-8') as file:
					for line in lines:
						stripped_line = line.strip()
						
						# If the line is a comment or blank, write it directly
						if stripped_line.startswith('#') or not stripped_line:
							file.write(line)
							continue  # Move to the next line

						# Check and remember the separator type
						if not val_sep:
							if " = " in line:
								val_sep = " = "
							elif "=" in line:
								val_sep = "="

						# Identify and set the current section
						if stripped_line.startswith('[') and stripped_line.endswith(']'):
							section = stripped_line.strip('[]')
							file.write(line)  # Write section header
							continue

						# Write key-value pairs, preserving the value separator
						if val_sep and section and val_sep in line:
							key, current_value = line.split(val_sep, 1)
							key = key.strip()

							# Check if the key exists in the current section of the config
							if key in config[section]:
								# Write the updated key-value pair
								file.write(f"{key}{val_sep}{config[section][key]}\n")
							else:
								# Write the original line if the key isn't found
								file.write(line)
						else:
							# Write any line that doesn't match expected patterns
							file.write(line)
			
			# Lets check if filename is provided by check for its existence directly
			if _Path.isFile(fn):
				#print("DEUG file: " , cls._file_conf)
				# A conf file can only be read if it exists
				import configparser as _cfgp
				#this_config = _cfgp.ConfigParser(interpolation=None)
				this_config, lines_raw = read_with_comments(fn)

				# Preserve CaseSensitify
				#this_config.optionxform = str
				
				# Open file (TODO: I guess this is needed, not sure if this will mess up the save process)
				#this_config.read(fn)

				# Conf file exists, lets parse memory storage and pass it to configparse
				C=0
				MAX = len(cls._values)

				# Lets parse through memory storage
				#print("4 save loop")
				#print("DEUG - save loop: " , C, MAX)
				while C <= MAX:
					# Get current setting
					cur_sec = str(cls._sections[C])
					cur_key = str(cls._keys[C])
					cur_val = str(cls._values[C])
					#print("DEUG - save loop: " , C, MAX, cur_val)

					# Ensure section exist in conf file:
					if not this_config.has_section(cur_sec):
						this_config.add_section(cur_sec)

					# Update config parser values
					this_config.set(cur_sec, cur_key, cur_val)

					# Goto next setting
					C += 1
					if C == MAX: break	# TODO Weird, it does not work with: while C << MAX
				
				# DEBUG configparser content
				#print("\nSections and values before saving:\n")
				#val = invalid_func(asfd)
				#for section in this_config.sections():
				#	print(f"[{section}]")
				#	for key, value in this_config.items(section):
				#		print(f"{key} = {value}")

				# Write file using configparser
				#this_config.write(fn)
				#with open(fn, 'w') as configfile:
				#	this_config.write(configfile)
				write_with_comments(fn, this_config, lines_raw)

				return True
		return False
	