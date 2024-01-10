"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""


# These are only required (here) for relative path import
import os
import sys
from os.path import abspath, dirname, join
# Add the ASPIRE directory to the system path
aspire_dir = abspath(join(dirname(__file__), '..'))
sys.path.append(aspire_dir)

## Usualy, this would be only:
##		from aspire import Aspire as tui
#from aspire.aspire import Aspire as tui


#
#	AspireTUI
#
# Public
from AspireTUI import tui
from AspireTUI import StringUtils as stew
from AspireTUI import Lists
# Advanced
from AspireTUI.ColorAndText import cat
from AspireTUI.Classes.Config import conf
from AspireTUI.Classes.Config import winreg
from AspireTUI.Classes.Config import yaml
from AspireTUI.Classes import ConfigEditor
from AspireTUI.Classes import CrashLog
from AspireTUI.Classes import Log
from AspireTUI.Classes import Conf


# Aspire Internal
# Same as above, but with _<name> alias
from AspireTUI import settings
from AspireTUI import _PrintUtils as _put
from AspireTUI import _theme as _Theme
_theme_list = _Theme.list()
_theme = _Theme.get()



# Basic "Hello World"
tui.header("ASPIRE by (sea/sri-arjuna)", f"{stew.now()}")
tui.title("Hello World")
tui.print("Left", "Center", "Right")
tui.print()
tui.print("Lets load the AspireTUI config")
tui.wait(5,"Wait for it...")
aConf = Conf("AspireTUI.conf")


tui.press()
