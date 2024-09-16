import sys
from os.path import abspath, dirname, join
# Add the ASPIRE directory to the system path
aspire_dir = abspath(join(dirname(__file__), '..'))
sys.path.append(aspire_dir)
from ..AspireTUI import tui
#import 
#from .AspireTUI import tui
#from .AspireTUI.ColorAndText import cat

#dirname(".").
from ..AspireTUI import StringUtils as stew
#from .AspireTUI.Classes.Crashlog import CrashLog
#from .AspireTUI import _theme as Theme

#import importlib
#tui = importlib.import_module('AspireTUI.tui', "..")
#cat = importlib.import_module('AspireTUI.ColorAndText.cat', "..")
#stew = importlib.import_module('AspireTUI.StringUtils', "..")
#crashlog = importlib.import_module('AspireTUI.Classes.Crashlog', "..")
#Theme = importlib.import_module('AspireTUI_theme', "..")

print(stew.sec2time(75))
tui.wait(5)

from AspireTUI.Classes import log
_logging = log("C:\test.txt")
_logging.Settings.LogLevel_ShowUser = _logging.LEVEL.WARN
_logging.info('Opening file %r, mode = %r', "FiLnAmE", "MoDe")
