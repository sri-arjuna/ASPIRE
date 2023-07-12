"""
	Created on:		2023.July.11
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""


# Imports
from enum import Enum

# Internals
from .aspire_data_color_and_text import cat

# Original symbols:
# ✓ ✗ ≣ ◆ ◇

"""
	Sadly, these seems not to work

	U+2713	✓	Check mark
	U+2714	✔	Heavy check mark
	U+2715	✕	Multiplication X
	U+2716	✖	Heavy multiplication X
	U+2717	✗	Ballot X
	U+2718	✘	Heavy ballot X
"""

class StatusEnum(Enum):
    Good = f"{cat.colors.front.green}{cat.text.bold}√{cat.reset}"
    Bad = f"{cat.colors.front.red}{cat.text.bold}X{cat.reset}"
    Todo = f"{cat.colors.front.cyan}{cat.text.bold}≡{cat.reset}"
    Work = f"{cat.colors.front.yellow}{cat.text.bold}∞{cat.reset}"
    Skip = f"»"
    Next = f">"
    Prev = f"<"
    On  = f"{cat.colors.front.green}{cat.text.bold}●{cat.reset}"
    Off = f"{cat.colors.front.red}{cat.text.bold}○{cat.reset}"

dict_status =  {
    '0': f"{StatusEnum.Bad}",
    '1': f"{StatusEnum.Good}",
    'False': f"{StatusEnum.Bad}",
    'True': f"{StatusEnum.Good}",
    '10': f"{StatusEnum.Off}",
    '11': f"{StatusEnum.On}",
    '2': f"{StatusEnum.Todo}",
    '3': f"{StatusEnum.Work}",
    '4': f"{StatusEnum.Skip}",
    '5': f"{StatusEnum.Next}",
    '6': f"{StatusEnum.Prev}",
}