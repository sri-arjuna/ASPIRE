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

class EnumStatus(Enum):
    Good = f"{cat.colors.front.green}{cat.text.bold}√{cat.reset}"
    Bad = f"{cat.colors.front.red}{cat.text.bold}X{cat.reset}"
    Todo = f"{cat.colors.front.cyan}{cat.text.bold}≡{cat.reset}"
    Work = f"{cat.colors.front.yellow}{cat.text.bold}∞{cat.reset}"
    Skip = f"»"
    Next = f">"
    Prev = f"<"
    On  = f"{cat.colors.front.green}{cat.text.bold}●{cat.reset}"
    Off = f"{cat.colors.front.red}{cat.text.bold}○{cat.reset}"
    