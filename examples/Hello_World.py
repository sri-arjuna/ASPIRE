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

# Usualy, this would be only:
#		from aspire import Aspire as tui
from aspire.aspire import Aspire as tui


# Basic "Hello World"
tui.header("ASPIRE by (sea/sri-arjuna)", "TODO TIME")
tui.title("Hello World")
tui.print("Left", "Center", "Right")
tui.press()