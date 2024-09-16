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
from AspireTUI import tui
from AspireTUI._PrintUtils import STATUS
#from aspire.aspire_data_status import dict_status


tui.header("Simple Data Presentation")
tui.title("Progress Bar")

tui.progress("Shows a bar: 1/10", 0.1, 1)
tui.progress("Shows a bar: 1/3", 1, 3)
tui.progress("Shows a bar: 1/2", 1, 2)

tui.title("User Interactions")
yesno = tui.yesno("Are you happy?")
if yesno:
    tui.status(STATUS.Done, "Yes you are")
else:
    tui.status(STATUS.Fail,  "No, you are not happy.")
tui.print()

tui.title("Does also work with base bool / and + INT ")
tui.status(yesno, "Bool result")
tui.status(10 + yesno, "Int result: On/Off = 10+Bool")

sys.exit()
#tui.print()
#tui.title("Call by dict")
#for key in dict_status:
    # It requires specificly INT or BOOL, since i'm just parsing key's here, they're any and wont work
    # So I had to fallback using EVAL, eventhough that is not recomended.
#    tui.print(f"tui.status({key}, 'Some text'", f"[ {eval(dict_status[key]).value} ]")

tui.print()
tui.title("Call by Enum")
for es in STATUS:
    tui.status(es, f"tui.status({es}, 'Message to user')")
