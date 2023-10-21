import random
import matplotlib.pyplot as plt
import numpy as np


class Direction:
    def __init__(self, direction_coords, coords_to_check, coords_to_color, path_coords):
        self.direction_coords = direction_coords
        self.coords_to_check = coords_to_check
        self.coords_to_color = coords_to_color
        self.path_coords = path_coords

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
    plt.imshow(matrix.T, cmap='gray_r', extent=[0, matrix.shape[0], 0, matrix.shape[1]], aspect='equal')
    plt.xticks(np.arange(0, matrix.shape[0]+1, 1))
    plt.yticks(np.arange(0, matrix.shape[1]+1, 1))
    plt.grid(True, which='both', color='black', linewidth=0.5)
    plt.show()


def extend_maze(board):


    # after this, do dead end filling. basically the same as before. pick random point, try extending a dead-end
    # when no valid points remain, maze is done.



    # Add all 1's to an array of "valid_points"
    valid_points = np.argwhere(board == 1)

    # Pick one random point from "valid_points"
    random_point = valid_points[random.randint(0, len(valid_points) - 1)]


    directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    valid_directions = []

    for direction in directions:

        new_x = random_point[0] + direction[0]
        new_y = random_point[1] + direction[1]

        if 0 <= new_x < board.shape[0] and 0 <= new_y < board.shape[1]:
            value = board[new_x, new_y]
            if value == 0:
                valid_directions.append(direction)
            print(value)

    direction_objs = []
    for direction in valid_directions:
        path_coords = []
        cells_to_check = []
        cells_to_color = []
        if direction[0] == 0:
            for i in range(-2, 3):
                path_coords.append([0 if i == 0 else int(i / abs(i)), direction[1]-1])
                cells_to_check.append([i, direction[1]])
                cells_to_check.append([i, direction[1]+1])
                cells_to_color.append([0 if i == 0 else int(i / abs(i)), direction[1]])

        else:
            for i in range(-2, 3):
                path_coords.append([0 if i == 0 else int(i / abs(i)), direction[1] - 1])
                cells_to_check.append([direction[0], i])
                cells_to_check.append([i, direction[1]+2])
                cells_to_color.append([direction[0], 0 if i == 0 else int(i / abs(i))])

        path_coords = [[a + b for a, b in zip(inner_list, random_point)] for inner_list in path_coords]
        direction_coords = [a + b for a, b in zip(direction, random_point)]
        coords_to_check = [[a + b for a, b in zip(inner_list, random_point)] for inner_list in cells_to_check]
        coords_to_color = [[a + b for a, b in zip(inner_list, random_point)] for inner_list in cells_to_color]

        direction_objs.append(Direction(direction_coords=direction_coords,
                                        coords_to_check=coords_to_check,
                                        coords_to_color=coords_to_color,
                                        path_coords=path_coords))


        for i in range(len(direction_objs)):
            if not direction_objs[i].validate_direction(board):
                del direction_objs[i]

    if len(direction_objs):
        random_direction = random.randint(0, len(direction_objs) - 1)

        for x, y in direction_objs[random_direction].coords_to_color:
            board[x][y] = 1
        x, y = random_point
        board[x][y] = 0

    return board


def create_checkered_board(x, y):
    board = np.zeros((x, y), dtype=int)
    board[1::2, ::2] = 1
    board[::2, 1::2] = 1
    return board

# Sample 2D array to test the function
checkered_maze = create_checkered_board(25, 15)

width = 25
height = 15

board = np.zeros((width, height), dtype=int)
middle_col = height // 2
board[:, middle_col] = 1

for i in range(100):
    board = extend_maze(board)
# display_maze(checkered_maze)
display_maze(board)
print("done")