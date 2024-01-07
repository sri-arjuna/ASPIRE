import sys
from os.path import abspath, dirname, join
# Add the ASPIRE directory to the system path
aspire_dir = abspath(join(dirname(__file__), '..'))
sys.path.append(aspire_dir)

from AspireTUI import tui
from AspireTUI.ColorAndText import cat
import AspireTUI._theme as Theme
from AspireTUI import StringUtils as stew

print(stew.sec2time(75))
