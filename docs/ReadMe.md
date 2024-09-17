![Logo](https://github.com/sri-arjuna/Aspire/blob/master/docs/img/ASPIRE_Logo.png?raw=true)

Achieving Seamless Performance In Real-time Environments -> Text User Interface
===============================================================================

> **Note:** \
> This is the official rewrite of TUI/SWARM by the original inventor/author Simon Arjuna Erat. \
> Please be aware that this is an unstable work in progress, and some references in this text may refer to habits/behaviour based on the original BASH source code.

* This software/framework is running under [MIT License](https://github.com/sri-arjuna/Aspire/blob/master/docs/LICENSE.txt)
* For recent updates, please see the [ChangeLog](https://github.com/sri-arjuna/Aspire/blob/master/docs/ChangeLog.md)
* You can install this as a [PyPi Package](https://pypi.org/project/AspireTUI/) --> ``pip install AspireTUI``
* Documentation and Source Code can be found on the [GitHub repo](https://github.com/sri-arjuna/Aspire)
* This framework has currently [![Downloads Month](https://static.pepy.tech/badge/AspireTUI/month)](https://pepy.tech/project/AspireTUI) with a total of [![Downloads](https://static.pepy.tech/badge/AspireTUI)](https://pepy.tech/project/AspireTUI) so far. (stats from pypi)

>> __Please report bugs and/or inconsistencies!__ \
>> --> [GitHub Issues](https://github.com/sri-arjuna/ASPIRE/issues) <--


Brief
-----
ASPIRE is a Python 3.11+ module that offers an easy to use line-based text user interface framework.

It aims to make the console output more appealing to end users and provide developers an easy to use framework for 'everyday tasks' and to put their output left, center and right oriented with some 'dividers' (header, title) using a theme for presentation.

> __Note:__\
> The original BASH version was only using internal BASH functionality and GNU Core Utils, I intend to only rely on Python standard library for this framework as well. \
> __No depency hell!__ *But I might need to "*re-invent the wheel*" for certain functions.* -> However, during WIP phases, I might rely on additional libs until my mind is ready to do so.


Target Audience
---------------
For developers aiming to enhance the user experience with the console.

![HelloWorld](https://github.com/sri-arjuna/Aspire/blob/master/docs/img/HelloWorld.jpg?raw=true)


Detail
------

ASPIRE is designed with simplified usability in mind for both end users and developers. \
These functions aim to streamline interactions and improve the overall experience, coding and usage wise.

It aims to be cross platform compatible, but this will also require you to handle certain cases in your own code.

### It supports:
* Any console that can run Python code.\
Like:
	* MS Windows (regular + PowerShell)
	* Any GNU + *nix system/distro \
	As a side effect this (partialy) includes:
		* Apple iOS


Usage & Preview
---------------

___Please see [help](https://github.com/sri-arjuna/Aspire/blob/master/docs/Help.md) and [examples](https://github.com/sri-arjuna/Aspire/blob/master/docs/examples) for detailed information.___

The code for the previous preview would look as simple as this, which is how you can use it as library in your projects:

```py
from AspireTUI import tui
from AspireTUI import Strings as _stew

tui.header("Aspire by (sea/sri-arjuna)", "{_stew.now()}")
tui.title("Hello World")
tui.print("Left string", "Center string", "Right string")
tui.wait(3)
tui.press()
```

This is how "Hello World" (using ``header``, ``title`` and ``print``) can look like:

![HelloWorld](https://github.com/sri-arjuna/Aspire/blob/master/docs/img/HelloWorld.jpg?raw=true)

![User Interactions](https://github.com/sri-arjuna/Aspire/blob/master/docs/img/yesno_status.jpg?raw=true)


Installation
------------

Super simple:
```
pip install AspireTUI
```


Various themes:
---------------

This is just a preview of the "official" themes.

You can further customize the appearance by using the ``Custom`` theme.

___Please see [help](https://github.com/sri-arjuna/Aspire/blob/master/docs/help) and [examples](https://github.com/sri-arjuna/Aspire/blob/master/docs/examples) for detailed information.___

![Themes Preview](https://github.com/sri-arjuna/Aspire/blob/master/docs/img/themes.jpg?raw=true)
