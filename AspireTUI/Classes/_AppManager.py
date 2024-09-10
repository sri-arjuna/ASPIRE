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
			iShowUser: int=2,
			iSaveLog: int=1,
			encoding: str="UTF-8",
			log_format: str="%F %H:%M:%S.%f",
			ext_log: str="log",
			ext_conf: str="cfg",
			chr_sep: str="=",
			chr_sect: str="[]",
			chr_comm: list=["#", ";"],
			theme: str="Default",
			theme_color: str=None,
			theme_style: str=None,
			status_separators: str="[]"
			):
		"""# Handle conf- & logfiles

# Usage:

from AspireTui.Classes import App

myAppName = App("myAppName")

myAppName.write()

myAppName.DEBUG("This goes to the logfile, but is NOT shown to user)

myAppName.INFO("If 'iShowUser=1' then this would be shown to user with a green check mark.)

myAppName.FATAL("This goes to the logfile, and is shown to user with a red exclamation mark.")

bDaily = myAppName.get("Log", "bDaily")

myAppName.set("myApp", ConfName, Value)

myAppName.set("myApp", ConfName, Value, doLog=True, Verbose=True)

### Arguments
base_filename:	\t	\t

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
					iShowUser: int=2,
					iSaveLog: int=0,
					encoding: str="UTF-8",
					log_format: str="%F %H:%M:%S.%f",
					ext_conf: str="cfg",
					ext_log: str="log",
					chr_sep: str="=",
					chr_sect: str="[]",
					chr_comm: list=["#", ";"],
					theme: str="Default",
					theme_color: str=None,
					theme_style: str=None,
					status_separators: str="[]"
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
				self.iShowUser: int= iShowUser
				self.iSaveLog: int= iSaveLog
				self.encoding = encoding
				self.log_format = log_format
				self.ext_conf = ext_conf
				self.ext_log = ext_log
				self.chr_sep = chr_sep
				self.chr_sect = chr_sect
				self.chr_comm = chr_comm
				self.theme = theme
				self.theme_color = theme_color
				self.theme_style = theme_style
				self.status_separators = status_separators
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
			iShowUser = iShowUser,
			iSaveLog = iSaveLog,
			encoding = encoding,
			log_format = log_format,
			ext_conf = ext_conf,
			ext_log = ext_log,
			chr_sep = chr_sep,
			chr_sect = chr_sect,
			chr_comm = chr_comm,
			theme = theme,
			theme_color = theme_color,
			theme_style = theme_style,
			status_separators = status_separators
		)
		# Init
		import configparser as _cfgp
		from .. import Path as _Path
		from .. import OS as _OS
		self.tui = _tui
		
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
		
		# Create filenames from passed base_filename
		self._file_conf = f"{self._file_dir}/{self.__get_name_conf()}"
		self._file_log = f"{self._file_dir}/{self.__get_name_log()}"
		
		# Is it a daily log?
		if self._self.bDaily:
			if not _Path.exists(self._file_log):
				# Create logfile if it does not exist
				self.__create_log()
		
		# Read config file data
		self.read()
	#
	#	Tools
	#
	def __get_name_log(self):
		"""
		Returns the generated log name, or None
		"""
		if self._self.base_filename:
			# Prepare varnames
			n = self._self.base_filename
			s = self._self.base_section
			l = self._self.ext_log
			t = _stew.date().replace(".","_")
			
			# Sanity check
			if not n:
				if not s:
					return False
				else:
					n = s
			
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
	
	def __create_log(self):
		"""
		Writes the heading comment of the logfile.

		If bDisableLog = True, the heading comment is appended to messages.
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
		"""
		message: str=None
		if self._self.bDefaultComment:
			message = f"{_VersionInfo.FileGenComment}\n"
			message += f"Conffile created for '{self._self.base_filename}' on {_stew.now()}"
		if self._self.comment_conf:
			# Its not none, overwriting default message
			message = self._self.comment_conf
		# Actually write the logfile
		with open(self.__get_name_conf(),"a",encoding=self._self.encoding) as fn:
			for msg in message.split("\n"):
				print(f"# {msg}", file=fn)

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
	
	#
	# 	LOG functions
	#
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
	
	#
	#	Conf functions
	#
	def read(cls, bSaveFirst: bool=False):
		"""
		Reads the configuration file and applies AspireTUI settings.
		"""
		# TODO: Remove the bSaveFirst arg for AppManager.read()??
		if bSaveFirst:
			cls.save()

		# Get config name
		fn = cls.__get_name_conf()
		logfile = cls.__get_name_log()

		#
		# Reset data containers
		# 
		cls._content = []
		cls._values = []
		cls._keys = []
		cls._sections = []

		# Function to remove leading and trailing quotes from strings
		def strip_quotes(value):
			if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
				return value[1:-1]
			return value
		
		#
		# Wrap around configparser
		#
		import configparser as _cfgp
		this_config = _cfgp.ConfigParser()
		# Preserve CaseSensitify
		this_config.optionxform = str
		# Open file
		this_config.read(fn)
		
		#
		# Fill Data containers
		#
		for s in this_config.sections():
			#print("DEBUBG: s", s)
			bla = this_config.options(s)
			#print("DEBUBG: keys", *bla)
			for key in bla:
				val = this_config.get(s,key)
				#print(f"DEBUBG: {s} {key} == ", val)
				cls._sections.append(s)
				cls._keys.append(key)
				cls._values.append(strip_quotes(val))
		
		# Some reused chars
		sep = cls._self.chr_sep
		sect = cls._self.chr_sect
		sec_cur = None
		sec_new = ""
		key = None
		
		# Read logfile raw
		if logfile:
			# Create logfile first - if required:
			if not _Path.exists(logfile):
				cls.__create_log()
				if cls._self.bVerbose: cls.DEBUG(f"cfg - Read: Created: {cls._file_log}")
		
		"""
		Lets handle public internal settings
		This refers to [AspireTUI]
		This is already parse and available in memory: _sections, _keys, _values
		"""
		# Lets retrieve the values first:
		T = "AspireTUI"
		this_theme		= this_config.get(T,"THEME")
		this_theme_color = this_config.get(T,"THEME_COLOR")
		this_theme_style = this_config.get(T,"THEME_STYLE")
		this_bdaily 	= this_config.get(T,"bDaily")
		this_savelog 	= this_config.get(T,"iSaveLog")
		this_showuser	= this_config.get(T,"iShowUser")

		# Apply values to _self from config -> overwrite 'defaults'
		if this_bdaily is not None : cls._self.bDaily = this_bdaily
		if this_savelog is not None : cls._self.iSaveLog = this_savelog
		if this_showuser is not None : cls._self.iShowUser = this_showuser
		# Special theme handling
		if this_theme_color is not None : cls._self.theme_color = this_theme_color
		if this_theme_style is not None : cls._self.theme_style = this_theme_style
		#print(cls._self.theme_style, cls._self.theme_color)

		#
		#	Theme handling
		#
		# Check for valid theme entry / value
		if this_theme is None : 
			this_theme = "Default"
		elif this_theme not in _tui._Theme.list() and this_theme.lower() != "random" and this_theme.lower() != "custom":
			this_theme = "Default"
		
		# Handle the theme
		lst_theme = list(_tui._Theme.list())
		#print(lst_theme)
		#print(this_theme)
		
		if "random" == str(this_theme).lower():
			# Check if random already had been applied
			if str(settings["theme"]).lower() != "random":
				import random
				rnd_theme = random.choice(lst_theme)
				cls._self.theme = rnd_theme
				# Apply theme that is neither "Default" nor literal "Random"
				settings["theme"] = rnd_theme
				_tui._Theme.set(cls._self.theme)
		elif "custom" == str(this_theme).lower():
			# This should apply the custom color and style to the _settings
			_tui._Theme.set("Custom", cls._self.theme_style, cls._self.theme_color)
			settings["theme"] = "Custom"
			settings["theme_color"] = this_theme_color
			settings["theme_style"] = this_theme_style
		else:
			cls._self.theme = this_theme
			_tui._Theme.set(cls._self.theme)
		
		# asdf
		return True
	
	def save(cls):
		"""
		Saves data to conf file.

		If only data related to [AspireTUI] (log) is available, it skips writing the file.
		"""
		# First, lets write all possible messages to log
		if cls.messages and cls._file_log:
			# Something is there
			if cls._self.bVerbose: cls.DEBUG(f"log - Save: Writing messages to: {cls._file_log}")
			with open(cls._file_log, "a", encoding=cls._self.encoding) as thisLOG:
				for entry in cls.messages: print(entry, file=thisLOG)


		# Ignore save conf, if only log/AspireTUI settings avvailable
		if len(cls.list_sections()) == 1 and "AspireTUI" in cls.list_sections() :
			# AspireTUI is the only section, nothing to do
			return False
		
		# Check every section
		for sec in cls.list_sections():
			# Easier find or add:
			sec_str =f"{cls._self.chr_sect[:1]}{sec}{cls._self.chr_sect[1:]}"
			#
			#	Section 1 
			#	Add new section if its not in content yet
			#
			if not sec_str in cls._content:
				# Not written yet
				cls._content.append(sec_str)
				# Lets add all keys of the section as well
				for key in cls.list_keys(sec):
					cur_str = f"{key}{cls._self.chr_sep}{cls.get(sec, key)}"
					cls._content.append(cur_str)
					if cls._self.bVerbose: cls.DEBUG(f"cfg - Save: Added to: {sec} || {key} = {cls.get(sec, key)}")
				next
			#
			#	Section 2 - Keys
			#	Found Section in content, lets update the keys or skip them
			#
			keys_not_found = []
			for key in cls.list_keys(sec):
				# Init
				val = cls.get(sec, key)
				key_str2 = f"{key}{cls._self.chr_sep}"
				key_str1 = f"{key_str2}{val}"

				# Get line/key index per key
				for line in cls._content:
					# Which lines to skip?
					if line != "":
						first = str(line)[0]
					else:
						# Nothing to work with
						next
					# Comments can be extensive and include examples, lets skip them
					if first in f"{cls._self.chr_sect}{cls._self.chr_comm}":
						# Sections are already handled
						# Comments could be handled here
						# This is just for minor performance gain - at best.
						# I mean, there are people who do like to write an
						# aweful lot of comments on rather short code that follows.
						# Just to demonstrate a point, occasionaly.
						# And for this example, I just want to illustrate and state,
						# that sometimes people do provide comments to their config
						# files, and thus those should remain, but also not be worked
						# with, as that could have the potential to slow down parsing.
						next
					#
					#	Section 2 - Keys
					#	Found Section in content, lets update the keys or skip them
					#
					# Start working
					if str(line).startswith(key_str2):
						# Good for replacing / reset text
						line_index = cls._content.index(line)
						val_old = cls._content[line_index]
						val_old = str(val_old).split(cls._self.chr_sep)[1]
						val_new = cls.get(sec, key)
						

						#print(f"old: {val_old} // val: {val}")
						#if str(val).strip() == str(val_old).strip():
						#if str(val).strip() == str(val_old).split(cls._self.chr_sep)[1].strip():
						if str(val).strip() == str(val_old).strip():
						#if key_str1 == str(cls._content[line_index]):
							# Its identical, nothing to do
							if cls._self.bVerbose: cls.DEBUG(f"cfg - Save: Skipping '{key_str1}'")
							#print(f"key: {key} // old: {val_old} // new: {val_new}")
							next
						else:
							# Value has changed, update it
							if cls._self.bVerbose: cls.DEBUG(f"cfg - Save: Updated to '{key_str1}' from '{val_old}'")
							cls._content[line_index] = f"{key_str1}"
							#print(f"key: {key} // old: {val_old} // new: {val_new} ... are NOT the same ?!")
							next
		#
		# 	Save finaly
		#
		try:
			cls.__create_conf()
			with open(cls._file_conf, "w", encoding=cls._self.encoding) as thisConf:
				content_str = "\n".join(cls._content)
				thisConf.write(content_str)
				if cls._self.bVerbose: cls.DEBUG(f"cfg - Save: All saved to: '{cls._file_conf}'")
				return True
		except:
			cls.ERROR(f"cfg - Save: There was an error saving: '{cls._file_conf}'")
			cls.__write_log(3, traceback.format_exc(4,True))
			return False
	def edit(cls):
		"""
		A  very basic menu for endusers to select their theme /or combo.
		"""
		ret_sel = None
		while True:
			_tui.clear()
			_tui.header("AspireTUI")
			_tui.title("Configuration Editor")
			ret_sel = _tui.pick(bMenu=True)
			if ret_sel == _tui._MSG.tui_list_back:
				# User wants to exit
				return 0
			_tui.print("TODO: Config Edit Menu")
			_tui.print("Needs to be added ")
	#
	#	Configuration tools
	#
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
	
	def get(cls, Section: str=None, Key: str=None, bVerbose=False):
		"""
		Raturns the value from the 'key=' of '[section]'
		"""
		# minimal verification for proper arguments
		#for s in cls._sections:
		#	print("DEBUG: sec", s)
		if Section in cls.list_sections() and Key in cls.list_keys(Section):
			pass
		elif Section is None or Key is None:
			msg = f"'AppMAnager.get()': {_tui._MSG.args_missing} / sec:{Section} / key:{Key}"
			cls.ERROR(msg)
			return False
		C=0
		cls.read()
		MAX = int(len(cls.list_sections()))
		out = False
		#print("DEBUG - MAX:", MAX)
		while C <= MAX:
			#print("DEBUG - C:", C)
			#print("DEBUG - sec:", cls._sections[C])
			#print("DEBUG - key:", cls._keys[C])
			
			if cls._sections[C] == Section and cls._keys[C] == Key:
				out = cls._values[C]
				break
			C+=1
		return out

	def set(cls, Section: str=None, Key: str=None, Value: str=None, bVerbose=False) -> bool:
		"""
		Set the value for the'[section]' with 'key=value'
		"""
		ret_bool = False
		if Section is None or Key is None or Value is None:
			msg = f"'AppMAnager.set()': {_tui._MSG.args_missing} / sec:{Section} / key:{Key} / var:{Value}"
			cls.ERROR(msg)
			return False
		
		# If not found, add a new entry
		if Key not in cls._keys:
			#cls._sections
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
			while C < MAX:
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
		if bVerbose: _tui.status(ret_bool, f"{Key}{cls._self.chr_sep}{Value}")
		return ret_bool
