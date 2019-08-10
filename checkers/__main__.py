from tkinter import Tk
from checkers.board import Board

if __name__ == "__main__":
    master = Tk()
    board = Board(master)
    master.mainloop()