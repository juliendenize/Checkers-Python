from tkinter import *

class View(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        master.minsize(width=700, height=500)
        self.grid()
        self.canvas = Canvas(self, width=500, height=500)
        self.canvas.grid(row=0, column=0)

    def createChecker(self, x, y):
        return self.canvas.create_oval(x*50 + 10, y*50 + 10, (x+1)*50 - 10, (y+1)*50 - 10)
    
    def createSquare(self, x, y):
        return self.canvas.create_rectangle(x*50, y*50, (x+1)*50, (y+1)*50)
    
    def colorObject(self, item, color):
        self.canvas.itemconfigure(item, fill=color)