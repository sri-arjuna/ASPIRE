"""
	Provides some version info
"""
from . import Strings as _stew
Created = "2023.11.09"
Changed = "2024.09.17"
Major = 0
Minor = 5
Build = 1
Version = f"{Major}.{Minor}.{Build}"
FileGenComment = f"Created by AspireTUI ({Version} from {Changed}), https://github.com/sri-arjuna/ASPIRE" #on {_stew.now()}"
