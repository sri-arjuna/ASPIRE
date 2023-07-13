Data Interactions:
==================

In the first section we will handle how to show a ``progressbar``, ``yesno `` questions, and the presentation of ``status`` messages.

| Name 	   | Description |
|----------|-------------|
| progress | By default a basic progressbar, offering 2 alternative modes: <br>- ``style="num"`` = 'reduces' the progress to a basic number style: ``[ 2 /4 ]``<br>- ``style="dash"`` prints a simple 'animated dash' to indicate a process is running: ``\ - / \|`` ***(TODO / WIP)*** |
| yesno    | Ask a simple "yes or no" question.<br>It read 1 character and will return ``True`` for 'y' and ``False`` for 'n'.<br>For non-english coders, you can simply pass the equivalent of 'yn' as argument, and till use those as identifiers for 'yesno'. |
| status   | Great to show certain status messages based on *nix based "init" style.<br>It accepts INT, BOOL, and its own ``StatusEnum`` type to print the (mostly) colored symbols.


----

Preview: [[Sample code: Data_Interactions.py](../../..//examples/Data_Interactions.py)]

![YesNo-Status](./yesno_status.jpg)


Creating Menus:
===============

With all the "wizard style" appearance, you might want to provide some menu to your users.

We've got you covered:

| Name 	   | Description |
|----------|-------------|
| ask      | Just a basic wrapper for pythons ``input``
| select   | Will print a ``list`` and auto-return the 
| list     | Prints a list of all passed entries. Does accept:<br>- lists<br>- dict<br>- Enum<br>By default it shows regular INT numbering, but by using ``style=roman`` you can enforce roman-style numbering for a more classic style. |




WIP