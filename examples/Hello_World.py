"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""

#
#	Imports required for this example
#
from AspireTUI import tui
from AspireTUI import Strings as _stew

#
#	Other imports that could be used
#
#	Please be aware that the concept of _Capital-letter
#	is ment to avoid mis-conception with native python libraries, 
# 	as these are TUI related wrappers.
#
from AspireTUI import Lists as _Lists
from AspireTUI import Path as _Path
from AspireTUI import OS as _OS
from AspireTUI.ColorAndText import cat as _cat

#
# Basic "Hello World"
#
tui.header("ASPIRE by (sea/sri-arjuna)", f"{_stew.now()}")
tui.title("Hello World")
tui.print("Left String", "Center String", "Right String")
tui.print()

#
# Wait for 5 seconds and user interaction to close the app
#
tui.wait(5,"Wait for it...")
tui.press()
