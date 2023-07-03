Usage:
======

While ASPIRE provides many different functionalities for you to use,
in most cases, the following example for **Small Projects** is suitable for most daily tasks.

> Please keep in mind, this is NOT a help file, and only shows how to access functions while naming one probable example.

Small projects:
---------------

Since ASPIRE is a line based ***T***ext ***U***er ***I***nterface framework, it is highly recommended to import it ``as tui`` (alias) in all projects.

Frequency Expectation: Always

```py
from aspire import Aspire as tui

tui.header(str1, str2, str3)
tui.title("Hello World")
tui.printe(v_left, v_center, v_right)
```

----

Complex as needed:
==================

As I love to point out, ASPIRE is a framework, so it is highly customizable according to your needs.


String Utils:
------------

Some of ASPIRE's functions will be using these utility functions depending on their passed arguments. \
However, someones one might want to access these directly.

Since this class mixes strings up, stirrs them well and purrs out something very different, i think of this ``as stew`` (which is spoken like 'stu' anyway).

Frequency Expectation: Often

These functions return as ``str`` or ``int``, depending on their name.

```py
from aspire_utils_string import StringUitils as stew

# Examples (may vary until release)
stew.num2roman('5')  ## Returns "V"
stew.splitpath(StringFull="C:\temp\project",StringCut="C:\")        ## Returns "temp / project"
```

----

Themes:
-------


```py
from aspire_dc_theme import ThemeClass
from aspire_dc_theme import ThemeEnum
from aspire_dc_theme import Theme


```

You can even create / provide your own custom theme like this:
```py
custom_theme = ThemeClass(
    border_left="...",
    border_right="...",
    color_fg="...",
    color_bg="...",
    prompt_read="...",
    prompt_select="...",
    bar_empty="...",
    bar_half="...",
    bar_full="...",
    title_left="...",
    title_right="...",
    header_left="...",
    header_right="...",
    filler="..."
)

Theme.set_custom_theme(custom_theme)
```




----

Print Utils:
------------

For example one of the key functions [[``tui.printe``]](../aspire/aspire.py) is based on the [[``PrintUtils``]](../aspire/aspire_print_utils.py), for which is recommend the alias ``as put``. \
Which refers to: ***P***rint ***UT***ils, and also is also a word play based on its meaning, since it ```put's``` the output on the console.

While one usually should be able to fulfill all tasks with the functions provided by Aspire, maybe you want to achieve a more specialized output that I have not thought of (yet).

Frequency Expectation: Very Rare

These functions print to console and have ``None`` as return value.
```py
from aspire_utils_print import PrintUtils as put

# Examples (may vary until release)
put.print_border(style=full)
put.print_text("Hello, World!")

```