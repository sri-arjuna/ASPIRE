"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""

from .aspire_dc_colors import ColorsAndTextCodes as cat
from .aspire_dc_theme import Theme
import shutil
import os
import sys
import platform


def _create_custom_fd():
	if platform.system() == 'Windows':
		# None  # Not supported on Windows
		return sys.stderr
	elif platform.system() == 'Darwin':
		# macOS (similar to Linux)
		return os.fdopen(os.dup(sys.stderr.fileno()), 'w')
	else:
		# Linux
		return os.fdopen(os.dup(sys.stderr.fileno()), 'w')

def _get_terminal_width() -> int:
		terminal_size = shutil.get_terminal_size((80, 20))  # Default size if terminal size cannot be determined
		return int(terminal_size.columns)


class PrintUtils:
	theme = Theme.get()
	width = _get_terminal_width()
	_border_fd = _create_custom_fd()

	
	def _calc_pos_left(text) -> int:
		# Calculate the indentation based on the length of the text
		return abs(1 + len(PrintUtils.theme.border_right))
	
	def _calc_pos_center(cls, text) -> int:
		# Calculate the indentation based on the length of the text
		return abs(_get_terminal_width // 2 * 2 - (len(cat.remove_console_codes(text)) // 2) )
	
	def _calc_pos_right(cls, text) -> int:
		# Calculate the indentation based on the length of the text
		return abs(_get_terminal_width - len(cat.remove_console_codes(text)) - 1 - len(cls.theme.border_right))
	
	def cursor2pos(pos: int):
		# Move the cursor to column 0
		sys.stdout.write('\r')
		# Get width of terminal window
		width = _get_terminal_width()
		# Move the cursor to the desired column
		if pos > width:
			sys.stderr.write(f"pos: {pos} is longer than width: {width}.")
			return False
		if pos <= 0:
			sys.stderr.write(f"pos: {pos} must be 0 or larger.")
			return False
		else:
			sys.stdout.write('\033[{}D'.format(pos))
		sys.stdout.flush()
		return True
	
	@classmethod
	def _left(cls, text, end='\n'):
		# Print text aligned to the left with specified indention and end character
		pos = cls._calc_pos_left(text)
		cls.cursor2pos(pos)
		print(f"{cls.theme.color_fg}{text}{cat.reset}", flush=True, end=end)

	@classmethod
	def _right(cls, text, end='\n'):
		# Print text aligned to the right with specified indention and end character
		pos = cls._calc_pos_right(text)
		cls.cursor2pos(pos)
		print(f"{cls.theme.color_fg}{text}{cat.reset}", flush=True, end=end)

	@classmethod
	def _center(cls, text, end='\n'):
		# Print text centered with specified indention and end character
		pos = cls._calc_pos_center(text)
		cls.cursor2pos(pos)
		print(f"{cls.theme.color_fg}{text}{cat.reset}", flush=True, end=end)

	@classmethod
	def text(cls, *args, end='\n'):
		# Print text based on the number of arguments
		if len(args) == 0:
			return
		elif len(args) == 1:
			cls._left(args[0], end=end)
		elif len(args) == 2:
			cls._left(args[0], end='')
			cls._right(args[1], end=end)
		elif len(args) == 3:
			cls._left(args[0], end='')
			cls._center(args[1], end='')
			cls._right(args[2], end=end)

	@classmethod
	def border(cls, style='print'):
		if style == 'print':
			left_border = f"{cls.theme.color_fg}{cls.theme.border_left} "
			right_border = f"{cat.reset}{cls.theme.color_fg}{cls.theme.border_right}"
		elif style == 'header':
			left_border = f"{cat.bg_blue}{cls.theme.color_fg}{cls.theme.header_left}"
			right_border = f"{cat.reset}{cat.bg_blue}{cls.theme.color_fg}{cls.theme.header_right}"
		elif style == 'title':
			left_border = f"{cls.theme.color_fg}{cls.theme.title_left} {cat.invert}{cls.theme.color_fg}"
			right_border = f"{cat.reset} {cls.theme.color_fg}{cls.theme.title_right}"
		else:
			raise ValueError("Invalid style argument. Expected 'print', 'header', or 'title'.")

		print(f"{left_border}{cls.theme.filler * cls.width}{right_border}", file=cls._border_fd)

	