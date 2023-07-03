Structure of classes, for contributors
======================================

Please see [USAGE.md](./USAGE.md) on how to include and work with each class on a basic level.

If you want to go "in depth", please see the [HELP.md](./HELP.md) (local) or even the [online variant](https://www.github.com/sri-arjuna/ASPIRE/docs/HELP.md) if your code editor does not have a 'render mode' for markdown. 

```
ASPIRE
+ Incldues: 
	Apsire (as tui)
	= Provides:
		All functions for every day tasks.
		In 99,999% of all cases, you'll never need to include any of the other classes, 
		as their functions will be provided "as argument" to these functions, if you so desire.
	+ Includes:
		PrintUtils (as put)
		= Provides:
			Internal core functions to print all output
		+ Includes:
			Themes (as theme)
			= Provides functionality to change how output is presented
			+ Includes:
				Colors and TextCode (as cat)
				= Provides:
					Color and Text Codes, to change fore color, background color, 
					font attributes like bold, italic, underline,
					but also code to move a line up and down in console.
+ Offers:   
	StringUtils (as stew)
	= Provides:
		A multitude of string changing functions, like 'int' to roman, hex, oct - and back.
		Simple to use functions to transform seconds to date_cur, date_differ, time_cur, time_differ
		As well as many more things.
+ Offers:
	Environment (as envy)
	= Provides:
		Simple access to things that one might need, such as "path_current", "path_script", "arch", "os" 
```
