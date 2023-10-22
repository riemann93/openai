import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


class Direction:
    def __init__(self, direction_coords, coords_to_check, coords_to_color):
        self.direction_coords = direction_coords
        self.coords_to_check = coords_to_check
        self.coords_to_color = coords_to_color

    def validate_direction(self, board):
        rows, cols = board.shape  # Assuming 'board' is a NumPy array
        for x, y in self.coords_to_check:
            if x < 0 or y < 0 or x >= rows or y >= cols:
                return False  # Out of bounds
            if board[x, y] != 0:
                return False  # Not a 0 in the board

        for x, y in self.path_coords:
            if x < 0 or y < 0 or x >= rows or y >= cols:
                return False  # Out of bounds
            if board[x, y] != 1:
                return False  # Not a 1 in the path
        return True  # All checks passed

def display_maze(matrix):
    # display once initial line is made. update when:
    # - all valid points are found, mark them green
    # - chosen point is marked red, rest back to black
    # - once all cells are checked, mark valid green, invalid red.
    # - if all valid, expand maze in all black. else back to choosing another point. keep invalid point red.

    # color scheme:
    # 0: white
    # 1: black
    # 2: blue
    # 3: green
    # 4: red

    colors = [(1, 1, 1), (0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0)]
    cmap = mcolors.ListedColormap(colors)
    plt.clf()
    plt.imshow(matrix.T, cmap=cmap, vmin=0, vmax=4, extent=[0, matrix.shape[0], 0, matrix.shape[1]], aspect='equal')
    plt.xticks(np.arange(0, matrix.shape[0] + 1, 1))
    plt.yticks(np.arange(0, matrix.shape[1] + 1, 1))
    plt.grid(True, which='both', color='black', linewidth=0.5)
    plt.draw()
    plt.pause(1)



def extend_maze(board, random_point, valid_directions):
    direction_objs = []
    for direction in valid_directions:
        coords_to_check, coords_to_color, direction_coords, path_coords = investigate_direction(direction,
                                                                                                random_point)


    if len(direction_objs):
        random_direction = random.randint(0, len(direction_objs) - 1)

        for x, y in direction_objs[random_direction].coords_to_color:
            board[x][y] = 1
        x, y = random_point
        board[x][y] = 0

    return board


def investigate_direction(direction, random_point):
    path_coords = []
    cells_to_check = []
    cells_to_color = []
    if direction[0] == 0:
        for i in range(-2, 3):
            path_coords.append([0 if i == 0 else int(i / abs(i)), direction[1] - 1]) # this line does not work
            cells_to_check.append([i, direction[1]])
            cells_to_check.append([i, direction[1] * 2])
            cells_to_color.append([0 if i == 0 else int(i / abs(i)), direction[1]])

    else:
        for i in range(-2, 3):
            path_coords.append([0 if i == 0 else int(i / abs(i)), direction[1] - 1])
            cells_to_check.append([direction[0], i])
            cells_to_check.append([i, direction[1] * 2])
            cells_to_color.append([direction[0], 0 if i == 0 else int(i / abs(i))])
    path_coords = [[a + b for a, b in zip(inner_list, random_point)] for inner_list in path_coords]
    direction_coords = [a + b for a, b in zip(direction, random_point)]
    coords_to_check = [[a + b for a, b in zip(inner_list, random_point)] for inner_list in cells_to_check]
    coords_to_color = [[a + b for a, b in zip(inner_list, random_point)] for inner_list in cells_to_color]

    return Direction(direction_coords, coords_to_check, coords_to_color), path_coords


def get_valid_directions(board, random_point):
    directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    valid_directions = []
    for direction in directions:

        new_x = random_point[0] + direction[0]
        new_y = random_point[1] + direction[1]

        if 0 <= new_x < board.shape[0] and 0 <= new_y < board.shape[1]:
            value = board[new_x, new_y]
            if value == 0:
                valid_directions.append(direction)
                board[new_x, new_y] = 3
    return board, valid_directions


def choose_point(board):
    # change chosen point to value 2
    valid_points = np.argwhere(board == 1)
    random_point = valid_points[random.randint(0, len(valid_points) - 1)]
    # random_point = np.array([24, 7])
    board[random_point[0], random_point[1]] = 2
    return board, valid_points, random_point


def board_setup(width, height):
    board = np.zeros((width, height), dtype=int)
    middle_col = height // 2
    board[:, middle_col] = 1
    return board


def fill_board(board, coords, value):
    rows, cols = board.shape
    for x, y in coords:
        if 0 <= x < rows and 0 <= y < cols:
            board[x, y] = value

def validate_direction(board, coords_to_check):
    rows, cols = board.shape  # Assuming 'board' is a NumPy array
    for x, y in coords_to_check:
        if x < 0 or y < 0 or x >= rows or y >= cols:
            return False  # Out of bounds
        if board[x, y] not in [0, 3]:
            return False  # Not a 0 in the board
    return True

def validate_path(board, path_coords):
    rows, cols = board.shape
    for x, y in path_coords:
        if x < 0 or y < 0 or x >= rows or y >= cols:
            return False  # Out of bounds
        if board[x, y] not in [1, 2]:
            return False  # Not a 1 in the path
    return True  # All checks passed

if __name__ == "__main__":
    width = 25
    height = 15
    board = board_setup(width, height)
    plt.ion()
    display_maze(board)

    board, valid_points, random_point = choose_point(board)
    display_maze(board)
    board, valid_directions = get_valid_directions(board, random_point)
    display_maze(board)
    direction_objs = []
    for direction in valid_directions.copy():
        direction_obj, path_coords = investigate_direction(direction, random_point)
        direction_objs.append(direction_obj)
        fill_board(board, direction_obj.coords_to_check, 3)
        display_maze(board)
        if not validate_path(board, path_coords):
            print("path not valid!")
            valid_directions.remove(direction)
            coords_to_color = []
            index_to_remove = np.where((valid_points == random_point).all(axis=1))[0][0]
            valid_points = np.delete(valid_points, index_to_remove, axis=0)
            break
        if not validate_direction(board, direction_obj.coords_to_check):
            print("direction not valid!")
            valid_directions.remove(direction)
    print("whattup")
    if len(valid_directions):
        random_direction = random.randint(0, len(valid_directions) - 1)
        fill_board(board, valid_directions[random_direction].coords_to_color, 1)

    display_maze(board)
    board[board == 2] = 1
    board[board != 1] = 0
    display_maze(board)

    plt.ioff()  # Turn off interactive mode