Roadmap / TODO list:
====================


1. Split (or shorten) strings for proper output (header, title, print, status, ask, etc.)
2. Get rid of ``eval`` in status
2. Add / make use of: bar_half for more 'dynamic' appearance.



* fix _msg / _settings renames




------------------------------------------------------------------------------------------

> \
> Below are just notes for myself. <br>
>  <br>


# Make ASPIRE as module:

----

- [Module:](https://docs.python.org/3/tutorial/modules.html)
- [Packaging:](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/)
- [PEP8: Descriptive Names:](https://peps.python.org/pep-0008/#descriptive-naming-styles)
- [PEP8: Module level dunder names:](https://peps.python.org/pep-0008/#module-level-dunder-names)

----

# Test local:

To prepare a local Python project to mimic a module that you can import, you can follow these steps:

1. **Organize your project**: Structure your project's code into a directory that represents your module. Create a main directory for your project, and within that directory, create a subdirectory with the same name as your module.

2. **Create an `__init__.py` file**: Inside the subdirectory representing your module, create an `__init__.py` file. This file can be empty, or you can use it to initialize variables, import other modules, or define functions or classes specific to your module.

3. **Define module functionality**: Within the subdirectory, create one or more `.py` files that contain the code specific to your module. These files can contain functions, classes, or any other components that make up your module's functionality.

4. **Test your module locally**: In another Python script or interactive session, you can test importing your module. You'll need to ensure that the module's directory is included in your Python's module search path.

   - One way to achieve this is by appending the directory path to the `sys.path` list:
     ```python
     import sys
     sys.path.append('/path/to/your/module')
     ```
   - Alternatively, you can set the `PYTHONPATH` environment variable to include the directory path.

5. **Import your module**: Now you can import your module as you would with any other Python module:
   ```python
   import yourmodule

   # Access functions, classes, or variables from your module
   yourmodule.some_function()
   ```

By following these steps, you can create a local Python project that can be imported and used like a module. However, it's important to note that this approach is suitable for local development and testing purposes. If you want to distribute your module for others to use, you should consider packaging it properly, following the Python packaging guidelines and creating a distribution package that can be installed via `pip` or other package managers.

For more information on packaging and distributing Python modules, refer to the Python Packaging User Guide: https://packaging.python.org/guides/distributing-packages-using-setuptools/


---------------------


RTA — heute um 12:29 Uhr
assuming measure_performance() is defined inside a class that I instantiated as the variable engine

@contextmanager
def measure_performance(self, *args) -> None:
    start = perf_counter()
    try:
        yield
    finally:
        runtime = f'{perf_counter() - start:.2f}'
        if 'total' in args:
            self.logger.info(f'Total execution time: {runtime} seconds')
        else:
            self.logger.info(f'Execution time for {args[0]}: {runtime} seconds')


## ---------------------------------------------------------------------------------------


subprocess.run(["explorer", user_home], shell=True)


---------------------------
