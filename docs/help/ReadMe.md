Help Overview:
==============

While I understand that the concept of a line based text user interface might seem new to many, I truely belive that its use is very simple and straight forward.

Every console works the same, from top to bottom, per line.

That said, I've came up with an idea to use the console just like that, as a "progressing / procedual dialog window", by printing a border (top: header), and sides (print), while also providing some dividers (title) for a 'summarization' of data presented to users.



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
