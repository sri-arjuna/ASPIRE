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
from aspire.aspire_data_color_and_text import cat

# Check for subprocess usage:
#import subprocess
#result = subprocess.Popen("")
#subprocess.Popen('', shell=True)
#os.system("")

## Default output
print("------")
tui.header("Left", "TODO TIME")
tui.title("Hello World")
tui.print("Left", "Center", "Right")
print("------")

# Why does cat.text.bold not work?
bold_text = "\033[1mThis text is bold\033[0mcompare"
bold_v2 = f"{cat.text.bold} my text{cat.reset}compare"
print(bold_text)
print(bold_v2)
tui.print(bold_v2,bold_text)

# Change theme ??
from aspire.aspire_core import Theme as theme
from aspire.aspire_core import PrintUtils as put
from aspire.aspire_data_themes import ThemesList

#theme.set(theme.available_themes("Classic"))
#theme.set_custom(theme.set("Classic"))
#theme.current_theme = theme.set("Classic")
#theme.current_theme = theme.set(theme.available_themes["Classic"])

tui.progress("Progres bar test:", 1, 3)
tui.progress("Progres bar test:", 1, 3, fstyle="num")

