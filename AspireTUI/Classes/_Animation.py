from enum import Enum as _Enum
from AspireTUI import tui

class _anims(_Enum):
	dash 	= [" | ", " / ", " - ", " \\ "]
	dots 	= ["     ", "    .", "   . ", "  .  ", " .   ", ".    " ]
	lines 	= ["_____", "____-", "___--", "__---", "_----", "-----", "----_", "---__", "--___", "-____", "_____" ]
	scan 	= ["-----", "---- ", "--- -", "-- --", "- ---", " ----", "-----", " ----", "- ---", "-- --", "--- -", "---- " ]


class Animation:
	def __init__(self, option=_anims.scan.value, custom: list = None, intervall=0.3):
		"""
			Plays a selectable string animation, or uses passed "custom" list.

			Options:

			- option:		Which animation to use:

			- custom:		Pass a list of strings that should be played through.

			- iIntervall:	This is only used when calling "myAnim.loop(How_Long_Secs: int)"

		"""
		# Get animation:
		if custom:
			self._anim_list = custom
		else:
			self._anim_list = option
		# Get animation length / max index
		self._anim_len = len(self._anim_list) - 1
		# Start with 0
		self._cur = 0
		self._intervall = intervall

	def loop(self, text: str = None, HowLong: int = 10):
		"""
		Plays animation at given intervall, for "HowLong"
		"""
		import time
		# TODO, send anim play to background
		while time.sleep(HowLong):
			while time.sleep(self._intervall):
				tui.print(text, self._show_next(),end="\r")
		# Newline
		print()

	def play(self, text: str = ""):
		"""
		"""
		tui.print(text, self._show_next())

	def _show_next(self):
		"""
		Internal, returns next animation and update value
		"""
		if self._cur >= self._anim_len:
			# End of anim reached
			self._cur = 0
		else:
			# Increase step
			self._cur += 1
		# Output:
		return self._anim_list[self._cur]
