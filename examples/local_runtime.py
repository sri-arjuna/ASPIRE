import sys
from os.path import abspath, dirname, join
# Add the ASPIRE directory to the system path
aspire_dir = abspath(join(dirname(__file__), '..'))
sys.path.append(aspire_dir)

from ..aspire_dir.AspireTUI import tui
from ..aspire_dir.AspireTUI.ColorAndText import cat
import ..aspire_dir.AspireTUI._theme as Theme
from ..aspire_dir.AspireTUI import StringUtils as stew

print(stew.sec2time(75))
tui.wait(5)
