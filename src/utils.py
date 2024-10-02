import os

def get_filename_from_filepath(filepath: str) -> str:
    """Extract the filename (without extension) from a given file path.
    Args:
        filepath (str): The full path of the file.
    Returns:
        str: The filename without the extension.
    """
    return os.path.splitext(os.path.basename(filepath))[0]
