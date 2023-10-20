import random
import matplotlib.pyplot as plt
import numpy as np


def display_maze(matrix):
    plt.imshow(matrix.T, cmap='gray_r', extent=[0, matrix.shape[0], 0, matrix.shape[1]], aspect='equal')
    plt.xticks(np.arange(0, matrix.shape[0]+1, 1))
    plt.yticks(np.arange(0, matrix.shape[1]+1, 1))
    plt.grid(True, which='both', color='black', linewidth=0.5)
    plt.show()


def create_maze(x, y):
    board = np.zeros((x, y), dtype=int)
    middle_col = y // 2
    board[:, middle_col] = 1

    # pick random point along the line
    # pick random valid direction (up or down in our first case)
    # extend the line one tile in a valid direction:
    # from:
    # 00000
    # 11111
    # 00000
    # to:
    # 01110
    # 11011
    # 00000

    # Continue until this process is not possible for any position.
    # Pick random point. if not possible, exclude point from availabe points to try.

    # after this, do dead end filling. basically the same as before. pick random point, try extending a dead-end
    # when no valid points remain, maze is done.

    # Add all 1's to an array of "valid_points"
    valid_points = np.argwhere(board == 1)

    # Pick one random point from "valid_points"
    random_point = valid_points[random.randint(0, len(valid_points) - 1)]
    x, y = random_point

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    valid_directions = []

    for x, y in directions:


    return valid_directions

    return board

def create_checkered_board(x, y):
    board = np.zeros((x, y), dtype=int)
    board[1::2, ::2] = 1
    board[::2, 1::2] = 1
    return board

# Sample 2D array to test the function
checkered_maze = create_checkered_board(25, 15)
maze = create_maze(25, 15)
# display_maze(checkered_maze)
display_maze(maze)
