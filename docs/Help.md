Help Intro & Overview:
==============

While I understand that the concept of a line based text user interface might seem new to many, I truely belive that its use is very simple and straight forward.

Every console works the same, from top to bottom, per line.

That said, I've came up with an idea to use the console just like that, as a "progressing / procedual dialog window", by printing a border (top: header), and sides (print), while also providing some dividers (title) for a 'summarization' of data presented to users.

All this while using a theme to "frame" the content and providing a slightly different appearance (just colors for the most part) to the end user.

### Important note

For the most up to date description of each and every function, please read the tooltip provided by your IDE.

* I have to admit that (to me) [MS Visual Studio Code](https://visualstudio.microsoft.com/downloads/) has become my most favorite IDE for coding, which is free for any and all projects. Dont forget to install PyLance for nice Python support.
* As an alternative, you could use [PyCharm by JetBrains](https://www.jetbrains.com/pycharm), which is free for OpenSource projects.
* Of course you can always use Notepad or [Notepad++](https://notepad-plus-plus.org/downloads/) (or any other IDE) but to my knowledge this does not support *dot notation* and/or reading/showing tooltip of modules/functions, which can be very helpful.

-------------------------------------------------------------------------------

### Index:

* tui
* Path
* OS
* Strings
* Lists
* Classes
  1. Conf
  2. Log
  3. AppManager
  4. Reg
* ColorAndText

-------------------------------------------------------------------------------

# T U I

	# In your project
	from AspireTUI import tui

	# Internal
	from AspireTUI import tui as _tui

*As the name suggests, this is probably is the core module for all your projects*

### Resources (TODO)

* [Examples]()
* [Youtube]()


### Functions

| Name | Description |
|------|-------------|
| header	| Will print a blue background accross the whole console 'surrounded' by borders.<br>It will accept up to 3 strings.|
| title		| Will print the borders, and fill the space in between with the foreground color (white),<br> and use the background color for the font.<br>This function accepts only 1 string, which will be printed in the center of the line.|
| print		|  Standart output, prints borders in foreground color and accepts up to 3 strings.<br>Will allign them as follows:<br>1. Left<br>2. Left,  Right<br>3. Left, Center, Right |
| ask		| Printing borders and the passed question, encapsules the default ``input``, returns the input. |
| yesno		| Similar to ``ask``, but will only accept yes/no, returns according bool. |
| pick		| Pass a list as argument, uses ``list`` to print them. Returns the string of the shown/entered number. |
| list 		| Used by ``pick`` to print a number to each item of the list |
| progress 	| Provides a progress bar with different options that can be used within the project. |
| press 	| You can pass a custom string to be displayed instead of: "Press ENTER key to continue." 
| status	| Shows status/retval in *nix-init-style and an optional message, returns passed error level (int, bool)
| wait 		| Waits X amount of seconds and displays remaining time. You can pass int or float, and change the time to minutes or hours.
| clear		| Clears the console screen and moves text cursors to top left corner.
| open 		| Opens passed file, folder or url with the default application for that task

-------------------------------------------------------------------------------

# P a t h

	# In your project
	from AspireTUI import Path

	# Internal
	from AspireTUI import Path as _Path

*Wrapper module, the capital letter is so it does not get confused with the standard Python library.*

Many functions provide these arguments:
* bVerbose=Bool == shows result to user
* bDual=Bool == returns bool and message

### Resources (TODO)

* [Examples]()
* [Youtube]()


### Functions

| Name | Description |
|------|-------------|
| dir_cur	| Returns the absolute current working directory in *nix-style format (/)
| dir_app 	| Returns the absolute path of the app that is running / calling this function
| exists	| Returns bool, can show filename (default) or full path to user
| is_file_in_use 	| Attempts to detect if file is currently in use/open (works more reliale on *nix systems)
| list_content 		| Returns a pre-sorted "container" to acccess: dirs, files, hidden files (leading '.' on *nix systems and/or hidden attribute on Windows systems).
| hasFiles 	| Looks for pattern in path and returns bool if found.
| gen_filename | Generates/return basename of filename : {fn_base}.{fn_ext}
 

### FileSystem checks:

*These are also used by ``exists`` and on succss will report the "type" in that message.*

| Name | Description |
|------|-------------|
| isFile 	| Returns bool
| isDir 	| Returns bool
| isLink 	| Returns bool
| isMount 	| Returns bool

-------------------------------------------------------------------------------

# O S

	# In your project
	from AspireTUI import OS

	# Internal
	from AspireTUI import OS as _OS

*Wrapper module, the capital letter is so it does not get confused with the standard Python library.*

Many functions provide these arguments:
* bVerbose=Bool == shows result to user
* bDual=Bool == returns bool and message

### Resources (TODO)

* [Examples]()
* [Youtube]()

### Functions

| Name | Description |
|------|-------------|
| get_dir_OS	| This should return a list of paths related to the current OS
| IS_GUI		| Bool
| isVerOS		| This will return the OS version, make sure you know what OS type you are on to not confuse Windows with Kernel version.
| isVerPy		| Float. Checks if the Python version is at least "minimal". If no "minimal" is provided, at least 3.9 is expected.


-------------------------------------------------------------------------------

# S t r i n g s

	# In your project
	from AspireTUI import Strings

	# Internal
	from AspireTUI import Strings as _stew

*Wrapper module, the capital letter is so it does not get confused with the standard Python library.*

Why ``stew``? Because it mixes up strings like a well stirred and delicious stew!

Many functions provide these arguments:
* bVerbose=Bool == shows result to user
* bDual=Bool == returns bool and message

### Resources (TODO)

* [Examples]()
* [Youtube]()

### Functions

| Name | Description |
|------|-------------|
| date		| Returns date in international format: YEAR.MONTH.DAY
| time		| Returns time in international 24 hour format: 15:30
| now		| Returns date / time as: 2024.12.30 / 15:45
| logtime	| 
| close_html_tags		| (Supposed to) Closes any open html tags in passed string
| esc2hex	| Transforms internal color codes to web-hex-colors.
| conf2dict		| Splits the content of a conf file (passed as string), or env/set outputs to a dictionary
| sec2time		| Transforms given seconds to proper HH:MM:SS format.
| num2roman		| Converts an integer to Roman numeral
| roman2num		| Converts Roman numeral to integer
| char2morse	| Converts characters or a multiline string to Morse code.
| morse2char	| Converts Morse code to characters.
| num2alpha		| Convert an integer to alphabetical representation.
| alpha2num		| Convert alphabetical representation to an integer.
| strip_quotes	| Removes leading and tailing quotes (") from a string

## The following functions most likely will be moved to their own according class.

### Functions - Registry

| Name | Description |
|------|-------------|
| reg_value_get		| Attempts to read passed arguments and returns the according value.
| reg_value_set		| Attempts to set passed value and returns a bool.
| reg_value_list_key		| Attempts to list all key inside passed key_path, returns them as list.
| reg_value_list_var		| Attempts to list all variable names inside passed key_path, returns them as list.
| 		| 
| 		| 

### Functions - ini / conf

| Name | Description |
|------|-------------|
| ini_read		| Reads c_file as ini file, looks for c_keys (section) and returns the value of c_variable.
| ini_write		| Writes c_file as ini file, looks for c_keys (section) and returns the value of c_variable.
| ini_list_keys		| Reads c_file as an ini file and returns a list of all section names.
| ini_list_vars		| Reads c_file as an ini file, looks for c_key (section), and returns a list of all variable names in that section.
| 		| 
| 		| 

-------------------------------------------------------------------------------

# L i s t s

	# In your project
	from AspireTUI import Lists

	# Internal
	from AspireTUI import Lists as _Lists

*Wrapper module, the capital letter is so it does not get confused with the standard Python library.*

Many functions provide these arguments:
* bVerbose=Bool == shows result to user
* bDual=Bool == returns bool and message

### Resources (TODO)

* [Examples]()
* [Youtube]()

### Functions, well... lists, dictionaries and Enums

| Name | Description |
|------|-------------|
| LOG_LEVEL			| Enum: Dot notation by name, returning int
| LOG_SEVERITY		| List: of loglevel names sorted by LOG_LEVEL
| roman_roman2num	| Dict: Pass roman returns int
| roman_num2roman	| Dict: Pass int returns roman
| morse_code		| Dict: Pass char/letter, returns Morse
| 		| 
| 		| 
| 		| 
| 		| 
| 		| 
| 		| 


-------------------------------------------------------------------------------

# C l a s s e s

	# In your project
	from AspireTUI import Classes
	from AspireTUI.Classes import {AppManager | Conf | Log | Reg}

	# Internal
	from AspireTUI import Classes as _Classes

*Wrapper module, the capital letter is so it does not get confused with the standard Python library.*

Many functions provide these arguments:
* bVerbose=Bool == shows result to user
* bDual=Bool == returns bool and message

### Resources (TODO)

* [Examples]()
* [Youtube]()

### Classes - AppManager

	# Minimal with non-default theme
	myApp = Classes.AppManager("MyAppName", theme="Elegance")
	
	# For convenience, ``get`` and ``set`` will always expect a section named ``MyAppName`` (whatever you pass as your apps name)
	val = myApp.get("Key")

*This class is a wrapper for (aka: unifies/ 2 in 1) Conf & Log classes, and allows to ease change the theme.*

Be aware that you can customize the log and config file extension, both ase on the passed MyAppName. No spaces are allowed for that string.



__For a full list of the functions, please read the functions of Conf and Log accordingly.__

| Name | Description |
|------|-------------|
| get_custom | This allows you to access non "MyAppName" sections
| set_custom | This allows you to access non "MyAppName" sections


### Classes - Conf

	# If no filename is passed you can still use it access/manage "runtime settings"
	myConf = Classes.AppManager("MyAppName.ini")

*This class is a wrapper for (aka: unifies/ 2 in 1) Conf & Log classes, and allows to ease change the theme.*

| Name | Description |
|------|-------------|
| get		| Returns value of passed ``Section, Key``
| set		| Set ``value`` for ``Key`` in ``Section``
| list_sections	| Returns a list of sections
| list_keys		| Returns a list of keys of passed section
| read			| Reads the config file to memory
| write			| Writes the config file from memory
| 			| 
| 			| 


### Classes - Log

	# If no filename is passed you can still use it to show certain messages according to the according SEVERITY.
	myLog = Classes.AppManager("MyAppName.log", iShowUser=2, iSaveLog=0)

*This class is a wrapper for (aka: unifies/ 2 in 1) Conf & Log classes, and allows to ease change the theme.*



| Name | Description |
|------|-------------|
| DEBUG		| Prints/Saves passed messaged according to iSaveLog and iShowUser
| INFO		| Prints/Saves passed messaged according to iSaveLog and iShowUser
| WARNING	| Prints/Saves passed messaged according to iSaveLog and iShowUser
| ERROR		| Prints/Saves passed messaged according to iSaveLog and iShowUser
| CRITICAL	| Prints/Saves passed messaged according to iSaveLog and iShowUser
| FATAL		| Prints/Saves passed messaged according to iSaveLog and iShowUser
| write		| Think of this as an Export, as it requires a filename to be passed if no filename was passed on init.
| 			| 


### Classes - Reg

	myReg = Classes.Reg(HKEY, Path)

*Only works on MS Windows*


| Name | Description |
|------|-------------|
| todo		| todo

-------------------------------------------------------------------------------

## O L D

-------------------------------------------------------------------------------


Basics:
-------

To introduce the basic usage / key elements of the framework to present output to the user, you might want to read into:

### Hellow World
- Help: [[1. HelloWorld](1.HelloWorld/)]
- Sample Project: [[HellowWorld.py](../../examples/Hello_World.py)]


### Comfort:

Of course there are interactions wiht users, not only by presenting progress to users, but also to recieve user input.

To do so, you can use the wrappers provided by ASPIRE.

- Help: [[2. Data Interactions](2.Data_Interactions/)]
- Sample Project: [[Data_Interactions.py](../../examples/Data_Interactions.py)]



W I P
======


Intermediate:
-------------

In most cases, you probably dont need any of these, as these functions (most often) provide certain behaviours to the key functions provided by ``from aspire import Aspire as tui``.

However, depening on your intentions, they might offer additional tools to fine tune the appearance and / or behaviour of your projects.


### Print Utils

These very much are for internal use:


### String Utils




Advanced:
---------

### Themes

While you do not have to care about the use of a theme, you can use one of the other themes if you think it'll match the style for your project more.

You can even create your own themes, or allow users to change the theme (among provided ones) if you want to support that.

- Help: [[Themes](Themes/)]
- Sample Project: [[ThemePreview.py](../../examples/ThemePreview.py)]



---------------------------------------------------------------

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
---------------------------------------------


---------------------------------------------------------------




To name a few of these convenient functions:\
All descriptions are based on the default theme.

| Name | Description |
|------|-------------|
| header	| Will print a blue background accross the whole console 'surrounded' by borders.<br>It will accept up to 3 strings.|
| title		| Will print the borders, and fill the space in between with the foreground color (white),<br> and use the background color for the font.<br>This function accepts only 1 string, which will be printed in the center of the line.|
| print		|  Standart output, prints borders in foreground color and accepts up to 3 strings.<br>Will allign them as follows:<br>1. Left<br>2. Left,  Right<br>3. Left, Center, Right |
| ask		| Printing borders and the passed question, encapsules the default ``input``, returns the input. |
| yesno		| Similar to ``ask``, but will only accept yes/no, returns according bool. |
| select	| Pass a list as argument, uses ``list`` to print them. Returns the string of the shown/entered number. |
| list 		| Used by ``select`` to print a number to each item of the list |
| bar 		| Provides a progress bar with different options that can be used within the project. |
