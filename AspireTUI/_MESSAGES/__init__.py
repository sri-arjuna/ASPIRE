"""
Description:
		Contains languages
Usage:
		from AspireTUI._MESSAGES import current as _MSG
		tui.ask( _MSG.tui_press_enter )

========================================================
Created on:		2024 Jan. 08
Created by:		Simon Arjuna Erat
License:		MIT
URL:			https://www.github.com/sri-arjuna/ASPIRE

Based on my TUI & SWARM for the BASH shell © 2011
"""
#
#	Language detection
#
# Currently only 1, so super easy
# TODO: once more are available, check:
#	system language
# 	aspire / project settings.
from . import english
current = english

