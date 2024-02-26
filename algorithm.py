import numpy as np
import random

backtrack_count = 0
# Determine if the value entered is valid
def is_valid(board, row, col, num):
    # Check row
    if num in board[row]:
        return False

    # Check col
    if num in board[:, col]:
        return False

    # Check 3x3 blocks
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

# Fill in the Sudoku
def fill_board(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                random_nums = list(range(1, 10))
                random.shuffle(random_nums)
                for num in random_nums:
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if fill_board(board):
                            return True
                        board[i][j] = 0
                return False
    return True


# Randomly Generated Sudoku
def generate_sudoku():
    board = np.zeros((9, 9), dtype=int)
    fill_board(board)
    # Randomly removes numbers
    for _ in range(40):  # Remove 40 numbers
        i, j = random.randint(0, 8), random.randint(0, 8)
        board[i][j] = 0
    return board


"""
Algorithm1: backtracking algorithm
"""
def solve_sudoku(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:  # Find a blank cell
                for num in range(1, 10):  # Try to fill in 1 to 9
                    if is_valid(board, i, j, num):
                        board[i][j] = num  # Assuming the fill-in is valid
                        if solve_sudoku(board):  # Move on to the next blank cell
                            return True
                        board[i][j] = 0  # Fill in invalid, backtracking
                return False  # Tried all the numbers. None of them work. Backtrack.
    return True  # All spaces are filled in and there are no conflicts


"""
Algorithm2: forward checking algorithm
"""
def solve_sudoku_with_forward_checking(board):
    # Initialize all possible values of the grid
    possibilities = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if board[i][j]:
                if not forward_checking(board, possibilities, i, j, board[i][j]):
                    return False  # No solution

    # recursive solver
    return solve_recursive(board, possibilities)


def forward_checking(board, possibilities, row, col, num):
    # Update Rows and Columns
    for i in range(9):
        if num in possibilities[row][i]:
            possibilities[row][i].remove(num)
        if num in possibilities[i][col]:
            possibilities[i][col].remove(num)

    # Updated 3x3 blocks
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if num in possibilities[start_row + i][start_col + j]:
                possibilities[start_row + i][start_col + j].remove(num)

    # Checking for the empty set, i.e. the case of no solution
    for i in range(9):
        for j in range(9):
            if not board[i][j] and not possibilities[i][j]:
                return False  # No possible number, no solution

    return True


def solve_recursive(board, possibilities):
    row, col = find_unassigned_location(board)
    if row is None and col is None:
        return True  # Solve

    for num in possibilities[row][col]:
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_recursive(board, possibilities):
                return True
            board[row][col] = 0  # Backtrack

    return False


def find_unassigned_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None, None



