"""
	Created on:		2023.July.09
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""

# These are only required (here) for relative path import
import sys
from os.path import abspath, dirname, join
# Add the ASPIRE directory to the system path
aspire_dir = abspath(join(dirname(__file__), '..'))
sys.path.append(aspire_dir)

from AspireTUI import tui
from AspireTUI.ColorAndText import cat
import AspireTUI._theme as Theme

# Loop all available themes
for thisTheme in Theme.list():
	Theme.set(thisTheme)
	tui.header(f"Selected: {thisTheme}", "TODO TIME")
	tui.title(f"{thisTheme} Theme")
	tui.print(f"Left: {cat.front.blue}{cat.back.light_yellow}blue on yellow", "Center", "Right")
	tui.press()
	print("")
