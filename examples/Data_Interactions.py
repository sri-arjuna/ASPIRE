# These are only required (here) for relative path import
import os
import sys
from os.path import abspath, dirname, join
# Add the ASPIRE directory to the system path
aspire_dir = abspath(join(dirname(__file__), '..'))
sys.path.append(aspire_dir)

# Import Aspire modules
# Usualy, this would be only:
#	from aspire import Aspire as tui
from aspire.aspire import Aspire as tui


tui.header("Simple Data Presentation")

tui.title("Progress Bar")
tui.progress("Shows a bar: 0/1", 0.1, 1)
tui.progress("Shows a bar: 1/3", 1, 3)
tui.progress("Shows a bar: 1/2", 1, 2)

tui.title("User Interactions")
yesno = tui.yesno("Are you happy?")