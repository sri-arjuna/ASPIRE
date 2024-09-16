# Try to run this localy?
bLocal = False
bShowMenu = False
if bLocal:
	# In Theory, this should work for local testing / debuging current code
	import os
	import sys
	aspire_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
	sys.path.append(aspire_dir)
	#os.chdir(aspire_dir)							# Just testing
	#print("DEBUB-ROOT:", os.path.abspath(os.curdir))
	#from .AspireTUI import tui 		### Supposed to be relative import, but package is taken....
	#from .AspireTUI import strings as stew
	#from .AspireTUI.ColorAndText import cat
	#v2
	#from . import tui
	#from . import cat
	#from . import stew
	# v3
	#import tui
	from ..AspireTUI import tui

else:
	# Regular import method, but obviously only from the installed package
	# So testing is a bit annoying / cumbersome.
	from AspireTUI import tui
	from AspireTUI import Strings as stew
	from AspireTUI.Strings import cat
	from AspireTUI import OS

# Top level menu, "<< Back" is added by the command
MENU = [
	"Status",
	"Progress",
	"String Splitting"
]

# Stupid Strings
msg1 = "Some really long string and most likely, and with a bit of hope, will need to be split so i can test the string split function and see if it works with the split at words."
msg = msg1 ; msg += msg1
msg2 = msg1 + msg1 + msg1
msg_simple = "a simple text that goes just slightly over the center of the console."

# Functions
def f_show_status():
	"""
	Parse through all options of status
	"""
	tui.status(False, "some longer", "additional text")
	for member in tui._put.STATUS:
		tui.status(member.value, f"Name: {member.name}", f"Value: {member.value}")

def f_show_progress():
	"""
	Parse through all options of progress
	"""
	tui.title("4 progress bars")
	tui.progress("Progres bar test:", 1, 3, style="num") ; print()	# Works
	tui.progress("some short text",6,7) ; print()					# Works
	tui.progress(f"{msg}{msg}",2,10)	; print()					# Works.. end
	tui.progress(f"{msg}{msg}",2,15,cut_from_end=False)	; print()					# center cut
	tui.progress("",218,750) ; print()									# Works
	tui.progress(f"{msg}{msg}",2,15)

def f_show_string_splitting():
	"""
	Parse through all options of string splits
	"""
	tui.title(f"Split title ---- {msg1}")
	tui.title("Splitting - 1 string, left")
	tui.print(msg)													# Works
	tui.title("Splitting - simple mode: 2")
	tui.print(msg_simple, msg_simple)								# Works
	tui.title("Splitting - 2 strings, L + R")
	tui.print(msg1, msg2)											# Works
	tui.title("Splitting - 3 strings, L, C, R - simple")
	tui.print(msg1, msg_simple, msg1)								# Works
	tui.title("Splitting - 3 strings, L, C, R")
	tui.print(msg1, msg1, msg1)										# Works

def f_show_welcome():
	"""
	Main loop
	"""
	while True:
		#tui.clear()
		tui.header(" AspireTUI, © 2023 by Simon Arjuna Erat (sea / sri-arjuna) ", f" {stew.now()} ")
		tui.title("Text formating included")
		tui.print("hello world", "it works")
		underline = f"{cat.text.underline}This text is underlined{cat.reset} compare"
		bold_v2 = f"This is {cat.text.bold}my bold text{cat.reset} example"
		italic = f"Should be: {cat.text.italic}italic"
		tui.print(bold_v2 , underline, italic)
		tui.title("--- M E N U ---")
		#
		# I present the MENU to you !!
		#
		sel_id, sel_str = None, None
		tui.list("a", "b" , "c", bRoman=True)
		tui.status(True, "a b c")
		sel_id, sel_str  = tui.pick(*MENU, bMenu=True, bDual=True)
		# Do action for picked selection
		if sel_id or sel_str:
			if 0 == sel_id:
				break # the loop
			if MENU[0] == sel_str:
				f_show_status()
			elif MENU[1] == sel_str:
				f_show_progress()
			elif MENU[2] == sel_str:
				f_show_string_splitting()
		else:
			tui.status(False, "Invalid selection: {sel_id} / {sel_str}")
		
		# Lets give the user time to read any menu output
		tui.press()
#
#	Execute Code as follows:
#
if bShowMenu:
	f_show_welcome()
else:
	# Basic checks
	#print("No args:")
	#tui.print()
	#tui.title()
	#tui.header()
	#tui.title()
	#tui.print()
	#print("with args:")
	#tui.title("a")
	#tui.header("a")
	#tui.header("a", "b", "c")
	


	

	LIST = [ "left", "center", "right", "something else", "and another entry"]
	if False:
		print(OS.isVerOS(bDual=True))
		print("-" * 120)
		
		# Lets start here
		from pathlib import Path as _Path
		import os
		
		value =  "%userprofile%" #"system32.dll"
		p = _Path(value)
		print("str: ", value)
		print("p: ", p)
		print("absolute: ",p.absolute())
		print("expand: ",p.expanduser())
		#print("p.os: ",os.path(p))
		#cl_file = r"C:\Users\necro\Documents\prjs\Skyrim\SSE-CLA\crash-2023-09-30-16-31-00.log"
		#tmp = _CrashLog(cl_file)
		#tui.title()
		#msg = "str %r L---R %r" % "abc" "123"
		#print(msg)
		
		from enum import Enum

		class MyEnum(Enum):
			OPTION1 = "Option 1"
			OPTION2 = "Option 2"

		def my_function(arg_with_list: MyEnum):
			# Your function logic here
			print(arg_with_list.name)

		my_function(arg_with_list=MyEnum.OPTION2)
	
		ret, msg = tui.pick(*LIST, bDual=True, bMenu=True)
		ret, msg = tui.status(ret, msg, bDual=True)
		#print(f"ret: {ret} // msg: {msg}")

		ret, msg = tui.yesno("Just testing", bDual=True, msg_no="You declined", msg_yes="You agreed")
		tui.status(ret, msg)
		tui.print("blabal")
	
		ret, msg = tui.pick(*LIST, bMenu=True, bDual=True, bVerbose=True)

tui.progress("Some text", 1.5, 7.0)
