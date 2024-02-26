import tkinter as tk
from tkinter import messagebox, font
import numpy as np
from algorithm import solve_sudoku, generate_sudoku, solve_sudoku_with_forward_checking
import time


class SudokuGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku")

        self.main_frame = tk.Frame(master)
        self.main_frame.pack(padx=10, pady=10)

        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.pack(side=tk.TOP)

        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # default_sudoku = np.array([
        #     [5, 3, 0, 0, 7, 0, 0, 0, 0],
        #     [6, 0, 0, 1, 9, 5, 0, 0, 0],
        #     [0, 9, 8, 0, 0, 0, 0, 6, 0],
        #     [8, 0, 0, 0, 6, 0, 0, 0, 3],
        #     [4, 0, 0, 8, 0, 3, 0, 0, 1],
        #     [7, 0, 0, 0, 2, 0, 0, 0, 6],
        #     [0, 6, 0, 0, 0, 0, 2, 8, 0],
        #     [0, 0, 0, 4, 1, 9, 0, 0, 5],
        #     [0, 0, 0, 0, 8, 0, 0, 7, 9]
        # ])

        # default_sudoku = np.array([
        #      [0, 2, 4, 3, 0, 0, 0, 0, 8],
        #      [0, 0, 0, 0, 0, 0, 0, 0, 6],
        #      [8, 0, 0, 0, 0, 0, 0, 5, 9],
        #      [0, 0, 0, 0, 1, 0, 9, 3, 4],
        #      [0, 0, 0, 0, 0, 0, 0, 0, 1],
        #      [0, 0, 0, 0, 4, 0, 0, 7, 0],
        #      [0, 0, 8, 1, 7, 0, 0, 0, 0],
        #      [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #      [0, 0, 6, 0, 0, 0, 0, 8, 3]
        # ])

        # default_sudoku = np.array([
        #     [9, 0, 0, 3, 0, 7, 0, 0, 5],
        #     [0, 0, 3, 0, 6, 9, 0, 2, 0],
        #     [0, 0, 0, 0, 0, 0, 9, 0, 7],
        #     [0, 5, 2, 0, 0, 8, 0, 0, 0],
        #     [0, 0, 0, 7, 5, 0, 0, 1, 0],
        #     [0, 0, 0, 0, 0, 6, 2, 0, 4],
        #     [0, 0, 4, 0, 7, 3, 0, 9, 0],
        #     [0, 7, 8, 0, 0, 0, 0, 0, 0],
        #     [2, 0, 0, 4, 0, 1, 0, 0, 6]
        # ])

        default_sudoku = np.array([
            [9, 0, 0, 2, 0, 0, 0, 0, 0],
            [0, 0, 5, 0, 0, 0, 0, 8, 0],
            [0, 6, 0, 0, 9, 4, 0, 0, 1],
            [0, 7, 0, 3, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 2],
            [8, 0, 0, 0, 7, 2, 0, 1, 0],
            [0, 9, 0, 0, 1, 7, 0, 0, 4],
            [0, 0, 0, 0, 3, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 9, 0, 0]
        ])

        self.initial_board = default_sudoku
        self.board = np.copy(self.initial_board)
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.custom_font = font.Font(family="Arial", size=12)

        for i in range(9):
            for j in range(9):
                bg_color = "#ffffff" if (i // 3 + j // 3) % 2 == 0 else "#cccccc"
                self.entries[i][j] = tk.Entry(self.board_frame, width=2, font=self.custom_font, justify='center',
                                              bg=bg_color, borderwidth=2)
                self.entries[i][j].grid(row=i, column=j, padx=1, pady=1)
                if self.initial_board[i][j] != 0:
                    self.entries[i][j].insert(0, str(self.initial_board[i][j]))
                # else:
                #     self.entries[i][j].insert(0, 0)

        self.solve_button = tk.Button(self.button_frame, text="Solve", command=self.solve, font=self.custom_font)
        self.solve_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset, font=self.custom_font)
        self.reset_button.pack(side=tk.RIGHT, padx=5)

    def solve(self):
        for i in range(9):
            for j in range(9):
                try:
                    val_str = self.entries[i][j].get()
                    val = int(val_str) if val_str else 0
                    self.board[i][j] = val if val in range(10) else 0
                except ValueError:
                    messagebox.showerror("Error", "Invalid input, please enter a number from 1-9")
                    return

        start_time = time.time()
        # Change algorithm here
        if solve_sudoku(self.board):
            end_time = time.time()
            solve_time = end_time - start_time
            print(f"Solving time: {solve_time} seconds")
            for i in range(9):
                for j in range(9):
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, str(self.board[i][j]))
        else:
            messagebox.showerror("Error", "Can't solve this sudoku.")

    def reset(self):
        new_board = generate_sudoku()
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if new_board[i][j] != 0:
                    self.entries[i][j].insert(0, str(new_board[i][j]))

