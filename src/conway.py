import numpy as np
import time
import os


class GameOfLife:
    def __init__(self, rows, cols):
        # Initialize the board with random cells
        self.board = np.random.choice([0, 1], size=(rows, cols), p=[0.5, 0.5])
        self.rows = rows
        self.cols = cols

    def display(self):
        os.system('cls')
        for row in self.board:
            print(''.join(['#' if cell else '.' for cell in row]))

    def get_next_generation(self):
        # Create a copy of the board to hold the next generation
        new_board = self.board.copy()

        for row in range(self.rows):
            for col in range(self.cols):
                # Count living neighbors
                neighbors = (self.board[(row - 1) % self.rows][(col - 1) % self.cols] +
                             self.board[(row - 1) % self.rows][col % self.cols] +
                             self.board[(row - 1) % self.rows][(col + 1) % self.cols] +
                             self.board[row % self.rows][(col - 1) % self.cols] +
                             self.board[row % self.rows][(col + 1) % self.cols] +
                             self.board[(row + 1) % self.rows][(col - 1) % self.cols] +
                             self.board[(row + 1) % self.rows][col % self.cols] +
                             self.board[(row + 1) % self.rows][(col + 1) % self.cols])

                # Conway's rules:
                if self.board[row][col] and (neighbors < 2 or neighbors > 3):
                    new_board[row][col] = 0
                elif not self.board[row][col] and neighbors == 3:
                    new_board[row][col] = 1

        # Set board to the new generation
        self.board = new_board

    def run(self, generations):
        for _ in range(generations):
            self.display()
            self.get_next_generation()
            time.sleep(0.1)


if __name__ == "__main__":
    game = GameOfLife(20, 50)
    game.run(200)
