from tkinter import *

class View(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        master.minsize(width=800, height=640)
        self.grid()
        self.canvas = Canvas(self, width=640, height=640)
        self.canvas.grid(row=0, column=0)
        self.sizeSquare = 80
        self.offsetPiece = 20

    def createChecker(self, x, y):
        return self.canvas.create_oval(x*self.sizeSquare + self.offsetPiece, y*self.sizeSquare + self.offsetPiece, (x+1)*self.sizeSquare - self.offsetPiece, (y+1)*self.sizeSquare - self.offsetPiece)
    
    def createSquare(self, x, y):
        return self.canvas.create_rectangle(x*self.sizeSquare, y*self.sizeSquare, (x+1)*self.sizeSquare, (y+1)*self.sizeSquare)
    
    def colorObject(self, item, color):
        self.canvas.itemconfigure(item, fill=color)

    def moveChecker(self, item, x, y):
        self.canvas.coords(item, x*self.sizeSquare + self.offsetPiece, y*self.sizeSquare + self.offsetPiece, (x+1)*self.sizeSquare - self.offsetPiece, (y+1)*self.sizeSquare - self.offsetPiece)
    
    def killChecker(self, item):
        self.canvas.delete(item)
    
    def changeIntoKing(self, item, x, y, color):
        self.canvas.delete(item)
        new_item = self.canvas.create_rectangle(x*self.sizeSquare + self.offsetPiece, y*self.sizeSquare + self.offsetPiece, (x+1)*self.sizeSquare - self.offsetPiece, (y+1)*self.sizeSquare - self.offsetPiece)
        self.colorObject(new_item, color)
        return new_item
