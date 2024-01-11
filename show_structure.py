import os
import importlib
from importlib.machinery import ModuleSpec
from importlib.util import module_from_spec

def custom_relpath(path, start):
    # Custom relpath function to handle long relative paths
    start_list = os.path.abspath(start).split(os.path.sep)
    path_list = os.path.abspath(path).split(os.path.sep)

    # Find the common prefix
    i = 0
    for i, (p1, p2) in enumerate(zip(start_list, path_list)):
        if p1 != p2:
            break

    # Calculate the relative path
    rel_path = os.path.sep.join(['..'] * (len(start_list) - i - 1) + path_list[i:])
    return rel_path

def parse_package(package_path, current_path="", result=None):
    if result is None:
        result = []

    for item in os.listdir(package_path):
        item_path = os.path.join(package_path, item)
        item_name, item_ext = os.path.splitext(item)

        if os.path.isdir(item_path):
            parse_package(item_path, f"{current_path}.{item_name}" if current_path else item_name, result)
        elif item_ext == ".py" and item_name != "__init__":
            result.append(f"{current_path}.{item_name}")

    return result

def import_item(item, package_path):
    full_path = os.path.join(package_path, *item.split("."))
    try:
        return importlib.import_module(item)
    except ImportError:
        # Handle directories by mimicking a module
        spec = ModuleSpec(name=item, loader=None, origin=full_path)
        return module_from_spec(spec)

if __name__ == "__main__":
    package_path = "AspireTUI"  # Adjust this to the actual path of the package

    items = parse_package(package_path)
    print(package_path)
    for item in items:
        module = import_item(item, package_path)
        rel_path = custom_relpath(module.__name__, package_path)
        print(f"  {rel_path[:-3]}")
        for name in dir(module):
            if not name.startswith("_"):  # Exclude private attributes
                print(f"    {item}.{name}")
