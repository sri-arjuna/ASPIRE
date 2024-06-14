"""
# Application Manager

*most simple handling for ini and log files*

from AspireTUI import Application

myApp = Application.Manager("MyApp")

myApp.DEBUG("Log level based output")

value = myApp.get("Section", "Key")

from AspireTUI import tui
tui._Theme.set("Tron")
tui.header()
tui.title("new conf")
-------------------------
CLASSIC.{get|set}[section,key,val]
CLASSIC.DEBUG("")
CLASSIC.save()

"""
# Imports
from .. import tui as _tui
from .. import Path as _Path
from .. import Strings as _stew
from .. import _VersionInfo
from ..Lists import LOG_LEVEL as LEVEL
from ..Lists import LOG_SEVERITY as SEVERITY
#
#	Defaults
#
_default_base_filename: str=None
_default_base_section: str=None
_default_bDefaultComment: bool=True
_default_bAutoRead: bool=True
_default_comment_conf: str=None
_default_comment_log: str=None
_default_bVerbose: bool=False
_default_bDaily: bool=False
_default_bDisableLog: bool=False
_default_iShowUser: int=2
_default_iSaveLog: int=0
_default_encoding: str="UTF-8"
_default_log_format: str="%F %H:%M:%S.%f"
_default_ext_log: str="log"
_default_ext_conf: str="ini"
_default_chr_sep: str="="
_default_chr_sect: str="[]"
_default_chr_comm: list=["#", ";"]
_default_theme: str="Default"

class AppManager:
	def __init__(self, 
			base_filename: str=_default_base_filename,
			base_section: str=_default_base_section,
			bDefaultComment: bool=_default_bDefaultComment,
			bAutoRead: bool=_default_bAutoRead,
			comment_conf: str=_default_comment_conf,
			comment_log: str=_default_comment_log,
			bVerbose: bool=_default_bVerbose,
			bDaily: bool=_default_bDaily,
			bDisableLog: bool=_default_bDisableLog,
			iShowUser: int=_default_iShowUser,
			iSaveLog: int=_default_iSaveLog,
			encoding: str=_default_encoding,
			log_format: str=_default_log_format,
			ext_log: str=_default_ext_log,
			ext_conf: str=_default_ext_conf,
			chr_sep: str=_default_chr_sep,
			chr_sect: str=_default_chr_sect,
			chr_comm: list=_default_chr_comm,
			theme: str=_default_theme
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
					comment_conf: str=None,
					comment_log: str=None,
					bVerbose: bool=False,
					bDaily: bool=False,
					bDisableLog: bool=False,
					iShowUser: int=2,
					iSaveLog: int=0,
					encoding: str="UTF-8",
					log_format: str="%F %H:%M:%S.%f",
					ext_conf: str="ini",
					ext_log: str="log",
					chr_sep: str="=",
					chr_sect: str="[]",
					chr_comm: list=["#", ";"],
					theme: str="Default"
					):
				self.base_filename = base_filename
				self.base_section = base_section
				self.bDefaultComment = bDefaultComment
				self.bAutoRead = bAutoRead
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
		# Assign values to class
		self._self = sub_self(
			base_filename=base_filename,
			base_section = base_section,
			bDefaultComment = bDefaultComment,
			bAutoRead = bAutoRead,
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
			theme = theme
		)
		from .. import Path as _Path
		from .. import OS as _OS
		# Init 
		self.tui = _tui
		self.tui._Theme.set(self._self.theme)
		self.Path = _Path
		self.OS = _OS
		self.messages = []
		self._content = []
		self._values = [] #DataContainer()
		#self._theme = theme
		# Simplify and verify
		if "/" in base_filename or "\\" in base_filename:
			# Has a regular path:
			self._file_dir = _tui._os.path.abspath(".")
		else:
			# No path provided, use current dir (usualy where the script/bin is)
			self._file_dir = _tui._os.path.abspath(".").replace("\\","/")
		self._file_conf = f"{self._file_dir}/{self.__get_name_conf()}"
		self._file_log = f"{self._file_dir}/{self.__get_name_log()}"
		#print(f"DEBUG: c:{self._file_conf} d:{self._file_dir} l:{self._file_log}")

		#self._values.set = set(self)
		#self._values.get = get(self)
		if self._self.bDaily:
			if not _Path.exists(self.__get_name_log()):
				self.__create_log()
		self.read()
		#for entry in self._values: # , self._self:
		#	print(f"* {entry}")
		
		#_tui.status(111, f"MAIN: Should have updated theme: {self._self.theme}")
		#self.__write_log = __write_log(self, *message)
	#
	#	Tools
	#
	def __get_name_log(self):
		"""
		Returns the generated log name, or None
		"""
		if self._self.base_filename:
			n = self._self.base_filename
			s = self._self.base_section
			l = self._self.ext_log
			t = _stew.date().replace(".","_")
			#filename = filename.replace(".log", f"-{_tui._stew.date().replace('.','_')}.log")
			if not n:
				if not s:
					return False
				else:
					n = s
			if self._self.bDaily:
				return f"{n}-{t}.{l}"
			else:
				return f"{n}.{l}"
		else:
			return None
	def __get_name_conf(self):
		"""
		Returns the generated conf name, or None
		"""
		if self._self.base_filename:
			n = self._self.base_filename
			c = self._self.ext_conf
			return f"{n}.{c}"
		else:
			return None

	def __create_log(self):
		"""
		Writes the heading comment of the logfile.

		If bDisaleLog = True, the heading comment is appended to messages.
		"""
		message: str=None
		if self._self.bDefaultComment:
			message = f"{_VersionInfo.FileGenComment}\n"
			message += f"Logfile created for '{self._self.base_filename}' on {_stew.now()}"
			message += f"\nDatetime                 Level        Type        Message"
		if self._self.comment_log is not None:
			# Its not none, overwriting default message
			message = self._self.comment_log
		# Write it?
		if self._self.bDisableLog or self.__get_name_log() is None:
			# No, just pre-save it
			for msg in message.split("\n"):
				self.messages.append(f"# {msg}")
		else:
			# Actually write the logfile
			with open(self.__get_name_log(), "a", encoding=self._self.encoding) as fn:
				for msg in message.split("\n"):
					print(f"# {msg}", file=fn)
			self.DEBUG(f"Log header created: {self.__get_name_log()}")
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
		err_msg = "To log a message, you must pass a level (int) and a message (str ;or;  STR_with_VAR_placeholder , VAR)."
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
	def read(cls):
		"""
		Reads the configuration file
		"""
		#_tui.status(111, f"READ: insdie")
		fn = cls.__get_name_conf()
		#
		# Read data raw
		# 
		cls._content = None
		cls._values = []
		if fn:
			if _Path.exists(fn):
				with open(fn, "r", encoding=cls._self.encoding) as thisConf:
					cls._content = thisConf.read()
			else:
				if not _Path.exists(cls.__get_name_log()):
					cls.__create_log()
					cls.DEBUG(f"Created: {cls._file_log}")
				return
		#
		# Parse raw data (_content) to usable data (_values)
		# 
		sec_cur = None
		sec_new = ""
		c=0
		if cls._content is None:
			# Nothing to do
			return
		for cont in cls._content.split("\n"):
			c+=1
			# Skip if comment
			doSkip = False
			if cont.startswith(cls._self.chr_comm[0]):
				next
			
			# Adjust if new section:
			if cont.startswith(cls._self.chr_sect[:1]):
				sec_new = cont.replace(cls._self.chr_sect[:1], "")
				sec_new = sec_new.replace(cls._self.chr_sect[1:], "")
				if sec_new != sec_cur and sec_new != "":
					sec_cur = sec_new
					sec_new = ""
					next
			
			# Since skip does not work for some reason...
			# Lets try this approach instead.
			sep = cls._self.chr_sep
			key = None
			if sep in cont:
				key = cont.split(sep)
			else:
				next
			
			# Add to _values
			if key:
				#val = f"{sec_cur} || {key[0]} == {key[1]}"	# val = {sec_cur, key[0]}
				#print(f"DEBUG {c}:: {sec_cur} || {key[0]} == {key[1]}")
				sect = cls._self.chr_sect
				key_use: str = key[0].replace(sect[:1],"")
				key_use: str = key_use.replace(sect[1:],"")
				var: str = key[1].replace('"',"")
				var: str = var.replace('\'',"")
				if not sec_cur == "AspireTUI":
					#print(f"{sec_cur} :: {key_use} = {var}")
					if key_use == "THEME":
						_tui._Theme.set(var)
						cls._self.theme = var
						cls.DEBUG(f"ini: Updated theme: {var}")
					if key_use == "bDaily":
						var: bool=bool(var)
						cls._self.bDaily = var
						cls._file_log = cls.__get_name_conf
						cls.DEBUG(f"ini: Daily log file: {var}")
					if key_use == "iShowUser":
						var: int=int(var)
						cls._self.iShowUser = var
						cls.DEBUG(f"ini: ShowUser messages: {SEVERITY[var]} / {var}")
					if key_use == "iSaveLog":
						var: int=int(var)
						cls._self.iSaveLog = var
						cls.DEBUG(f"ini: SaveLog messages: {SEVERITY[var]} / {var}")
					#pass
				cls.set(Section=sec_cur, Key=key_use, Value=var)
				#cls.DEBUG(f"ini -> _values :: sec:{sec_cur} / key:{key_use} / var:{var}")
	#
	#	Configuration tools
	#
	
	def get(cls, Section: str=None, Key: str=None, bVerbose=False):
		"""
		Raturns the value from the 'key=' of '[section]'
		"""
		pass
	def set(cls, Section: str=None, Key: str=None, Value: str=None, bVerbose=False):
		"""
		Set the value for the'[section]' with 'key=value'
		"""
		#def set(self, sector, key, value):
		if not isinstance(Section, str):
			Section = Key
			Key = Value
			Value = bVerbose
		if not Section or not Key or not Value:
			msg = f"'AppMAnager.set()': {_tui._MSG.args_missing} / sec:{Section} / key:{Key} / var:{Value}"
			cls.WARNING(msg)
			#_tui.status(False, msg)
			return False
		#if not cls._values:
		#	_tui.status(0, "Empty _values:") #_tui._MSG.)
		#	print(cls._values)
		#	return False
		
		# If not found, add a new entry
		if not cls._values:
			cls._values.append({'section': Section, 'key': Key, 'value': Value})
		else:
			# Update values
			for entry in cls._values:
				if entry['section'] == Section and entry['key'] == Key:
					entry['value'] = Value
					return


		