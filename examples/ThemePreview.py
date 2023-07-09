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


# Usualy, this would be only:
#		from aspire import Aspire as tui
from aspire.aspire import Aspire as tui
from aspire.aspire_data_color_and_text import cat
from aspire.aspire_core import Theme as theme


# Loop all available themes
for thisTheme in theme.available_themes:
        theme._selected = thisTheme
        theme.get()
        print(cat.clear)
        tui.header(f"Selected: {thisTheme}", "TODO TIME")
        tui.title(f"{thisTheme} Theme")
        tui.print("Left", "Center", "Right")
        tui.press()