from tkinter import Tk
from top_controller import Controller

if __name__ == "__main__":
    master = Tk()
    master.minsize(width=800, height=640)
    Controller(master).displayFirstMenu()
    master.mainloop()