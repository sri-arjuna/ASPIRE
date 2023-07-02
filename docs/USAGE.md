Usage:
======

While ASPIRE provides many different functionalities for you to use,
in most cases, the following example for **Small Projects** is suitable for most daily tasks.

Small projects:
---------------

Since ASPIRE is a line based text user interface framework, it is highly recommended to import it ``as tui`` (alias) in all projects.

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

For example one of the key functions [[``tui.printe``]](../aspire/aspire.py) is based on the [[``PrintUtils``]](../aspire/aspire_print_utils.py).

```py
from aspire_utils_print import UtilsPrint  # as up

PrintUtils.print_border(style=full)
PrintUtils.print_text("Hello, World!")

```

