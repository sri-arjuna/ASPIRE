ASPIRE: Achieving Seamless Performance In Real-time Environments
================================================================
> **Note:** \
> This is the official rewrite of TUI/SWARM by the original inventor/author Simon Arjuna Erat. \
> Please be aware that this is an unstable work in progress, and some references in this text may pertain to habits based on the original BASH source code.


Brief
-----
ASPIRE is a Python 3.3+ module that offers a line-based text user interface framework.


Detail
------
ASPIRE simplifies common tasks by providing various functions that wrap around frequently used code. It serves as a three-way interface between the system (MS Windows, any *Nix based system, and even Apple's iOS), the author/developer, and the end user.

One of ASPIRE's key focuses is to enhance the console experience by offering themable designs. You, as the author, can choose from a variety of ASCII-based themes that include colors, symbols, bold and underline fonts, and more. Users also have the option to select a different theme or even create their own.

ASPIRE is designed with simplified usability in mind for both end users and developers. It provides convenient functions such as `header`, `title`, `printe`, `ask`, `yesno`, `select`, `list` and `bar`. These functions aim to streamline interactions and improve the overall experience.


Target Audience
---------------
For developers aiming to enhance the user experience with the console.


----


Installation
------------

At least thats where i want to go:
```
pip install ASPIRE
```


Usage
-----

Use as library or via pyinstaller:

```py
from aspire import Aspire as tui

tui.header(str1, str2, str3)
tui.title("Hello World")
tui.printe(v_left, v_center, v_right)
```

For an example list of different use cases, please see: [USAGE](./docs/USAGE.md)

Example:
--------

![prewview](./docs/preview1.jpg)