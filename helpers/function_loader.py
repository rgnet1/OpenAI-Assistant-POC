import importlib
import os

def load_functions_from_directory(directory="functions"):
    """
    Dynamically loads and instantiates classes from Python files in a specified directory.

    Each Python file in the directory is expected to contain a single class. The name of the class
    should match the filename (without the '.py' extension).

    Args:
    directory (str): The directory to scan for Python files.

    Returns:
    dict: A mapping of function names to their run_function method from each class.
    """
    function_map = {}
    function_desc_list = []
    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Remove .py extension
            module_path = f"{directory}.{module_name}"
            
            # Dynamically import the module
            module = importlib.import_module(module_path)

            # Assuming class name matches the file name
            class_name = module_name

            # Instantiate the class
            func_class = getattr(module, class_name)()


            # Add to the function map
            function_map[func_class.name] = func_class.run_function

            # Set up funciton list
            function_desc_list.append(func_class.openai_func_desc)


    return function_map, function_desc_list