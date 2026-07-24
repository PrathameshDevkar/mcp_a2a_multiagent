import os

def load_instructions_file(filename: str, default : str = ""):
    """
    Load instructions from a file. If file doesnt exist return default instructions.

    Args:
        filename (str): The path to the instructions file
        defualt: Defult instructions to return if thje file does not exist.

    Returns:
        str: The content of the instructions file or the default instructions.
    """

    if os.path.exists(filename):
        with open (filename, "r", encoding = "utf-8") as f:
             return f.read()
    
    return default
