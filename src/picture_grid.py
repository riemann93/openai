import os

from PIL import Image, ImageDraw


def add_grid_to_image(image_path, output_path):
    # Open the image
    img = Image.open(image_path)
    width, height = img.size

    # Create a drawing object
    draw = ImageDraw.Draw(img)

    # Set grid line properties
    line_color = (255, 0, 0)  # red color
    line_width = 5  # thicker line width

    # Draw the horizontal grid lines
    for i in range(1, 4):
        y_position = i * (height / 4)
        draw.line([(0, y_position), (width, y_position)], fill=line_color, width=line_width)

    # Draw the vertical grid lines
    for i in range(1, 4):
        x_position = i * (width / 4)
        draw.line([(x_position, 0), (x_position, height)], fill=line_color, width=line_width)

    # Save the image with the grid
    img.save(output_path)


def list_files_in_current_directory(path=None):
    # Get the current directory's path
    if not path:
        path = os.getcwd()

    # List all files and directories in the current directory
    contents = os.listdir(path)

    for item in contents:
        print(item)


# Example usage
list_files_in_current_directory()
add_grid_to_image('..\\media\\messy_room.jpg', '..\\media\\messy_room_grid.jpg')
