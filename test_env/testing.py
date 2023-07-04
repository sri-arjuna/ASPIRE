"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""

import sys
from os.path import abspath, dirname, join

# Add the ASPIRE directory to the system path
aspire_dir = abspath(join(dirname(__file__), '..'))
sys.path.append(aspire_dir)

from aspire.aspire import Aspire as tui


tui.header("ASPIRE by (sea/sri-arjuna)", "", "TODO TIME")
tui.title("Hello World")
tui.print("Left", "Center", "Right")
tui.status("")
tui.press()
