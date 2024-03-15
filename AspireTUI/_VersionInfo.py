"""
	Provides some version info
"""
from . import Strings as _stew
Created = "2023.11.09"
Changed = "20242.03.03"
Major = 0
Minor = 2
Build = 3
Version = f"{Major}.{Minor}.{Build}"
FileGenComment = f"# Created by AspireTUI ({Version} / {Changed}), on {_stew.now()}"
