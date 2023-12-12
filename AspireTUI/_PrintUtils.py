"""
	Description:
					Internal functions for tui.*, handle string splitting and theme.
	Provides:
					put.border(style=header|title)			\n
					put.text(*args, style=header|title)

	========================================================
	Created on:		2023 Nov. 09
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE

	Based on my TUI & SWARM for the BASH shell © 2011
"""
################################################################################################################
#####                                            Shared Imports                                            #####
################################################################################################################
#
#	Essential imports
#
import os
import sys
import re
import string
# 
#	Cross Platform & Advanced usage
#
import platform
import msvcrt
import shutil
import subprocess
#
#	Prepare data structures
#
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum, EnumMeta
from typing import Union
#
#	Prepare for multi language support
#
import gettext #as _
from pathlib import Path
# Lang setup
translation_directory = Path("locales")
translation = gettext.translation("AspireTUI", translation_directory, fallback=True)
translation.install()
#
#	Internals
# 
from AspireTUI import settings, FD_BORDER #, IS_WINDOWS
import AspireTUI._internal as _internal
#import AspireTUI.StringUtils as stew
from AspireTUI.ColorAndText import cat
import AspireTUI._theme as Theme

#from AspireTUI import __internal
################################################################################################################
#####                                            Internal Functions                                        #####
################################################################################################################
def _width_terminal_raw() -> int:
	# Returns raw width of the console
	try:
		# This __SHOULD__ return 80 colums if it could not detect the actual value
		# But in all my tests, this did not work.. not at all..
		terminal_size = shutil.get_terminal_size((80, 20))
		return terminal_size.columns
	except (AttributeError, KeyError):
		# Fallback for cases where terminal size cannot be determined
		return 80  # Default width

def _width_full() -> int:
	# Returns rounded int of width_terminal_raw()
	return int(_width_terminal_raw() // 2 * 2)
	
def _width_inner() -> int:
	# Return width_full minus borders
	style = Theme.get()
	return settings["full"] - len(style.border_left) - len(style.border_right) - 2

def _update(forced=False, DEBUG=""):
	"""
	Internal use!		\n
	Updates settings["full"] and settings["inner"] every 5th tui.* call.		\n
	tui.header uses forced=True to ensure the best possible alignment for a new segment.		\n
	"""
	limiter = 10
	if forced:
		settings["due"] = limiter + 1
	if settings["due"] >= limiter:
		settings["full"] = _width_full()
		settings["inner"] = _width_inner()
		settings["due"] = 0
		#print(f"DEBUG-Update: full:{settings['full']} // inner:{settings['inner']} // width: {_width_inner()} // DEBUG: {len(DEBUG)} // txt: {DEBUG}")
	else:
		settings["due"] += 1
	
################################################################################################################
#####                                            Status                                                    #####
################################################################################################################
"""
	Sadly, these seems not to work

	U+2713	✓	Check mark
	U+2714	✔	Heavy check mark
	U+2715	✕	Multiplication X
	U+2716	✖	Heavy multiplication X
	U+2717	✗	Ballot X
	U+2718	✘	Heavy ballot X
"""
class _StatusEnum(Enum):
	Good = f"{cat.front.green}{cat.text.bold} √ {cat.reset}"
	Bad = f"{cat.front.red}{cat.text.bold} X {cat.reset}"
	Todo = f"{cat.front.cyan}{cat.text.bold} ≡ {cat.reset}"
	Work = f"{cat.front.yellow}{cat.text.bold} ∞ {cat.reset}"
	Skip = f" » "
	Next = f" > "
	Prev = f" < "
	On  = f"{cat.front.green}{cat.text.bold} ● {cat.reset}"
	Off = f"{cat.front.red}{cat.text.bold} ○ {cat.reset}"
	Info = f"{cat.front.yellow}{cat.text.bold}!!!{cat.reset}"

_dict_status = {
	'0': _StatusEnum.Bad,
	'1': _StatusEnum.Good,
	False: _StatusEnum.Bad,
	True: _StatusEnum.Good,
	'10': _StatusEnum.Off,
	'11': _StatusEnum.On,
	'2': _StatusEnum.Todo,
	'3': _StatusEnum.Work,
	'4': _StatusEnum.Skip,
	'5': _StatusEnum.Next,
	'6': _StatusEnum.Prev,
	'111': _StatusEnum.Info,
}

def status(ID: Union[int, bool]):
	if not isinstance(ID, (int, bool)):
		msg_status_bool_int = _("STATUS: ID should be an int or bool.")
		raise TypeError(msg_status_bool_int)
	try:
		return f"[ {_dict_status[ID].value} ]"
	except KeyError:
		msg_status_no_entry = _("STATUS: Could not find entry for: ")
		raise ValueError(msg_status_no_entry, f"{ID}")

#################################################################################################################
#####                                           Print Utils (_put)                                          #####
#################################################################################################################
def remove_console_codes(text) -> str:
	# Remove console/color codes from text
	if text is None:
		return ""
	return re.sub(r'\033\[[0-9;]+m', '', text)

def _calc_pos_left() -> int:
	style = Theme.get()
	# Calculate the indentation based on the length of the text
	return abs(2 + len(style.border_right))

def _calc_pos_center(text) -> int:
	# Calculate the indentation based on the length of the text
	return abs(settings["full"] // 2 - (len(remove_console_codes(text)) // 2) )

def _calc_pos_right(text) -> int:
	# Calculate the indentation based on the length of the text
	style = Theme.get()
	return abs(settings["full"] - len(remove_console_codes(text)) - len(style.border_right))

def _cursor2pos(pos: int, as_str=False):
	"""
	Internal use.												\n
	Moves the curso to POS on line.								\n
	Returns the according console code if "as_str=True"			\n
	"""
	# Move the cursor to column 0
	sys.stdout.write('\r')
	# Get width of terminal window
	width = settings["full"]
	# Move the cursor to the desired column
	if pos > width:
		sys.stderr.write(f"pos: {pos} is longer than width: {width}.")
		return False
	if pos < 0:
		sys.stderr.write(f"pos: {pos} must be 0 or larger.")
		return False
	else:
		if as_str:
			return f'\033[{pos}G'
		else:
			sys.stdout.write(f'\033[{pos}G')
			sys.stdout.flush()
			return

def _left(text, style='print', end='\n'):
	"""
	Internal use.			\n
	Returns text-string aligned to the left with specified indention and end character.			\n
	"""
	cur_theme = Theme.get()
	pos = _calc_pos_left()
	if "" == text:
		return ""
	#_cursor2pos(pos)
	if "header" == style:
		output = f"{cur_theme.color_fg}{cur_theme.color_bg}{text}{cat.reset}"
	else:
		output = f"{text}{cat.reset}"
	return f"{_cursor2pos(pos, True)}{output}"

def _right(text, style='print', end='\n'):
	"""
	Internal use.			\n
	Returns text-string aligned to the right with specified indention and end character.			\n
	"""
	cur_theme = Theme.get()
	if "" == text:
		return ""
	output = ""
	if text != "":
		pos = _calc_pos_right(text)
		if "print" == style:
			# Default, just font
			output = f"{text}{cat.reset}"
		elif "header" == style:
			# Regular bg, full
			output = f"{cur_theme.color_fg}{cur_theme.color_bg}{text}{cat.reset}"
	else:
		pass
	return f"{_cursor2pos(pos, True)}{output}"

def _center(text, style='print', end='\n'):
	"""
	Internal use.			\n
	Returnss text-string centered with specified indention and end character.			\n
	"""
	cur_theme = Theme.get()
	pre = ""
	if text != "":
		if "title" == style:
			text = f" {text} "
			pos = _calc_pos_center(text)
			if cur_theme.title_bold:
				pre += f"{cat.text.bold}"
			if cur_theme.title_underline:
				pre += cat.text.underline
			if cur_theme.title_italic:
				pre += cat.text.italic
		else:
			pos = _calc_pos_center(text)
		if "print" == style:
			# Default, just font
			output = f"{text}{cat.reset}"
		elif "header" == style:
			# Regular bg, full
			output = f"{cur_theme.color_fg}{cur_theme.color_bg}{text}{cat.reset}"
		elif "title" == style:
			# TODO fix: Invert colors
			output = f"{cur_theme.color_fg}{cur_theme.color_bg}{cat.codes.invert}{pre}{text}{cat.reset}"
		#print(f"{output}", flush=True, end=end)
		return f"{_cursor2pos(pos, True)}{output}"
	else:
		pass

def border(style='print'):
	"""
	Supposed for internal use, can be used by other developers.			\n

	Prints border or the full line according to passed style.			\n
	Accepts: header, title, print, status			\n
	"""
	cur_theme = Theme.get()
	#cur_theme. --- ChatGPT this is line 271
	width = settings["full"]
	if style == 'header':
		left_border = f"{cur_theme.color_fg}{cur_theme.color_bg}{cur_theme.header_left}"
		right_border = f"{cur_theme.color_fg}{cur_theme.color_bg}{cur_theme.header_right}{cat.reset}"
	elif style == 'title':
		left_border = f"{cur_theme.color_fg}{cur_theme.color_bg}{cur_theme.title_left}{cat.codes.invert}"
		right_border = f"{cat.reset}{cur_theme.color_fg}{cur_theme.color_bg}{cur_theme.title_right}{cat.reset}"
	elif style == 'print' or style == 'status':
		left_border = f"{cur_theme.color_fg}{cur_theme.color_bg}{cur_theme.border_left}{cat.reset}"
		right_border = f"{cur_theme.color_fg}{cur_theme.color_bg}{cur_theme.border_right}{cat.reset}"
	else:
		msg_invalid_style = _("Invalid style argument. Expected 'print', 'header', or 'title'. // passed: ")
		raise ValueError(msg_invalid_style, f"{style}")

	# Prepare filler chars / line
	if "header" == style:
		fill = cur_theme.header_filler
	elif "title" == style:
		fill = cur_theme.title_filler
	else:
		if "print" == style or style == 'status':
			fill = " "
	if fill == "":
		fill = " "
	
	# Print "filler"
	center = (width - 2 * len(cur_theme.border_left)) // 2 * 2  * fill

	# Print Border
	print(f"{_cursor2pos(0, True)}{left_border}{center}{right_border}", flush=True, file=FD_BORDER, end="")

def text(*args, **kwargs):
	"""
	Supposed for internal use, can be used by other developers.			\n
	Prints up to 3 strings L, LR, LCR 		\n
	Valid kwargs are: end, style={header/title/print/status} 
	"""
	# Get args -- ChatGPT, this is line 309
	style = kwargs.get("style", "print")
	end = kwargs.get("end", "\n")
	LineLength = settings["inner"]
	arg_count = len(args)
	if arg_count >= 4:
		print(_("Too many arguments"))
		return 1
	# Reset handle-vars
	L, C, R = "", "" , ""
	linesL, linesC, linesR = [], [], []
	need_split = False
	length_total = 0
	# Prepare values
	if len(args) > 0:
		for a in args:
			#print("DEbug split: ", len(a), a)
			if a == "":
				length_total += 0
			else:
				length_total += len(str(remove_console_codes(a)))
	if length_total > LineLength:
		need_split = True
	# Before we do anything, lets go back so we can properly print:
	if need_split:
		if 1 == arg_count:
			if "title" == style:
				w = LineLength * 0.5
				linesC = _internal.split_string_preserve_words(args[0], w)
				print(_center(linesC[0],style=style))
				border(style=style)
				text(linesC[1],style=style)
			else:
				# print and header
				w = LineLength * 0.8
				linesL = _internal.split_string_preserve_words(args[0], w)
				text(linesL[0], style=style)
				# 2nd line
				tmp = linesL[1]
				while len(tmp) > 0:
					tmp2, tmp3 = _internal.split_string_preserve_words(tmp, w)
					border(style=style)
					print(_right(tmp2, style=style))
					tmp = tmp3
			# Single args done
			return True
		if 2 == arg_count:
			# print and header
			if len(args[0]) < LineLength:
				# L fits on one line
				linesL = _left(args[0], style=style, end="")
				# R maybe too?
				if len(args[1]) < LineLength:
					# Yes, so easy mode
					linesR = _right(args[1], style=style, end="")
					# Output
					print(linesL) #, end="")
					border(style=style)
					text("", linesR, style=style)
				else:
					# Nope, needs 2 lines
					# More complex handling
					w = LineLength * 0.45
					linesR = _internal.split_string_preserve_words(args[1], w)
					# First line
					print(_left(linesL, style=style), _right(linesR[0], style=style))
					# Loop through remaining linesR
					tmp = linesR[1]
					while len(tmp) > 0:
						tmp2, tmp3 = _internal.split_string_preserve_words(tmp, w)
						border(style=style)
						print(_right(tmp2, style=style))
						tmp = tmp3 #[len(tmp2) + 1:].strip() # fix tailing space (len + strip)
				return True
			else:
				# L does not fit on one line.
				w = LineLength * 0.45
				linesL = _internal.split_string_preserve_words(args[0], w)
				linesR = _internal.split_string_preserve_words(args[1], w)
				len_todo = len(linesL[1]) + len(linesR[1])
				print(_left(linesL[0], style=style) , _right(linesR[0], style=style))

				# Loop for all remaining output:
				while len_todo > 0:
					L = linesL[1]
					R = linesR[1]
					linesL = _internal.split_string_preserve_words(L, w)
					linesR = _internal.split_string_preserve_words(R, w)
					if len(linesL) <= 1:
						return True
					len_todo = len(linesL[1]) + len(linesR[1])
					# Acctual output
					border(style=style)
					print(_left(linesL[0], style=style) , _right(linesR[0], style=style))
				return True
		elif 3 == arg_count:
			# Most complex - simple approach first.
			w = LineLength * 0.3
			count_simple = len(args[0]) + len(args[2])
			if count_simple < LineLength:
				# Simple approach should work:
				text(args[0], args[2], style=style)
				# Loop through remaining linesR
				tmp = linesC[1]
				while len(tmp) > 0:
					tmp2, tmp3 = _internal.split_string_preserve_words(tmp, w)
					border(style=style)
					linesC = _center(tmp2, style=style)
					print(linesC)
					tmp = tmp3

		# TODO
		#print("todo string splitting")
		DEBUG = f"{args}"
		print(f"DEBUG - print-split: full:{settings['full']} // inner:{settings['inner']} // length_total: {length_total} // txt: {DEBUG}")
		return "todo string splitting" #, args, LineLength, length_total)
		return False
	else:
		# Expected default behaviour:
		if arg_count == 3:
			L = _left(args[0], style=style, end="")
			C = _center(args[1], style=style, end="")
			R = _right(args[2], style=style, end="")
		elif arg_count == 2:
			#print("DEBUG: ",args)
			L = _left(args[0], style=style, end="")
			R = _right(args[1], style=style, end="")
		elif arg_count <= 1:
			if args[0] is None or args[0] == "":
				L = ""
			else:
				if style == "title":
					C = _center(args[0], style=style, end="")
				else:
					L = _left(args[0], style=style, end="")
		else:
			print(_("Holy guackamoly, you should never see this, please report!"))
			print("--> from put.text")
			return False
		print(f"{_cursor2pos(0, True)}{L}{C}{R}", end=end)
		return True

#
#		STEW	-->	__internal
#
	def print_part(part, align_func):
		if stew.split_needed(len(part), LineLength, 75, style=style):
			pos = stew.split_calc_char_pos(LineLength, 75)
			lines = stew.split_string_preserve_words(part, pos)
			align_func(lines[0], style=style, end="\n")
			border(style=style)
			align_func(lines[1], style=style, end=end)
		else:
			align_func(part, style=style, end=end)

	if "title" == style:
		split_percent = 50
		if split_percent <= 100 // LineLength * len(remove_console_codes(args[0])):
			pos = stew.split_calc_char_pos(LineLength, split_percent)
			lines = stew.split_string_preserve_words(args[0], pos)
			_center(lines[0], style=style, end="\n")
			text(lines[1], style=style, end="\n")
		else:
			_center(args[0], style=style, end=end)
	elif len(args) == 1:
		print_part(args[0], _left)
	elif len(args) == 2:
		print_part(args[0], _left)
		border(style=style)
		print_part(args[1], _right)
	elif len(args) == 3:
		if "status" == style:
			len_status = len(remove_console_codes(args[2]))
			if len(args[0]) < LineLength:
				border(style=style)
				print_part(args[0], _left)
				print_part(args[1], _center)
				print_part(args[2], _right)
			else:
				pos = stew.split_calc_char_pos(LineLength, 90)
				linesL = stew.split_string_preserve_words(args[0], pos)
				linesC = stew.split_string_preserve_words(args[1], pos)
				print_part(linesL[0], _left)
				border(style=style)
				print_part(linesL[1], _left)
				print_part(linesC[0], _center)
				print_part(linesC[1], _right)
				print_part(args[2], _right)
		elif stew.split_needed(len_arg, LineLength, 30, style=style):
			pos = stew.split_calc_char_pos(LineLength, 30)
			linesL = stew.split_string_preserve_words(args[0], pos)
			linesC = stew.split_string_preserve_words(args[1], pos)
			linesR = stew.split_string_preserve_words(args[2], pos)
			print_part(linesL[0], _left)
			print_part(linesC[0], _center)
			print_part(linesR[0], _right)
			border(style=style)
			print_part(linesL[1], _left)
			print_part(linesC[1], _center)
			print_part(linesR[1], _right)
		else:
			print_part(args[0], _left)
			print_part(args[1], _center)
			print_part(args[2], _right)


def bar(cur: int, max: int, width: int = settings["inner"], reverse: bool = False):
	"""
	Internal use. \n
	Returns a string to resemble a progressbar according to the used theme. \
	"width" is how long the bar must be in characters.
	"""	
	# Get filling characters:
	_update()
	style = Theme.get()
	e = style.bar_empty
	h = style.bar_half
	f = style.bar_full
	bar_empty, bar_half, bar_full = "", "", ""

	# Prepare vars:
	p_cur = 100 / max * cur					# Percentage
	p = format(100 * cur / max, ".2f")		# Percentage to show
	length = width - 2 - len(str(p)) - 2	# Rmove len of percentage from displayable width
	length_fill = int(length / 100 * p_cur)	# Get multiplier for fill-char

	tmp = p.split(".")[1]					# Get value after decimal
	if int(tmp) >= 50: bar_half = h			# Fill half if percentage > 50%
	bar_empty = e * int(length)				# Prepare bar-empty
	bar_full = f * int(length_fill)			# Prepare bar-filled

	# Prepare final string
	output = bar_empty[:-len(bar_full)]
	if bar_half: output = bar_empty[:-len(bar_half)]
	output = f"{bar_full}{bar_half}{bar_empty}"

	if reverse:
		return f"{p}% [{output}]"
	else:
		return f"[{output}] {p}%"
