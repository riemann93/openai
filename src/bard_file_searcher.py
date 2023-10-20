import os


def list_elements(folder, depth=1):
    """Lists all elements in a folder, to a specified depth.

    Args:
        folder: The path to the folder.
        depth: The depth to search to.

    Returns:
        A list of all elements in the folder and its subfolders, to the specified depth.
    """

    elements = []

    for root, dirs, files in os.walk(folder):
        for dir in dirs:
            if depth > 0:
                elements += list_elements(os.path.join(root, dir), depth - 1)

        for file in files:
            elements.append(os.path.join(root, file))

    return elements


# Example usage:

folder = r"C:/Users/Steffan/Torrents"
depth = 2

elements = list_elements(folder, depth)

for element in elements:
    print(element)
