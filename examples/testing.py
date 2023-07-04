import os
import sys


os.system("")


COLOR_RED = '\033[31m'
COLOR_GREEN = '\033[32m'
COLOR_YELLOW = '\033[33m'
COLOR_RESET = '\033[0m'
BACK_BLUE = '\033[44m'
BACK_MAGENTA = '\033[45m'
print_str = BACK_BLUE + COLOR_YELLOW + '/// --- This is yellow text.' + COLOR_RESET 

print(BACK_MAGENTA + '--PRINT ---' + print_str)
sys.stdout.write(BACK_MAGENTA + "---stdout---" + print_str)
sys.stdout.flush
#os.system(BACK_MAGENTA + "---os.system---" + print_str)
print("")


#from aspire.aspire_dc_colors import ColorsAndTextCodes as cat
#my_colors = cat.bg.cyan + cat.fg.white
#print(my_colors + "test string" + cat.reset)
