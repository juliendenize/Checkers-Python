from tkinter import Canvas, Frame, Tk

class View(Frame):
    """
        Represent the GUI

        Extends
        ----------
        Frame: the Frame class from the Tkinter librairy

        Attributes
        ----------
        canvas : Canvas
             The canvas holding the checker
        sizeSquare : int
            the size in pixel of a square in the board
        offsetPiece: int
            the offset of a piece in a square
    """
    def __init__(self, master):
        """
            Construct the view object

            Parameters
            ----------
            master: Tk
                Window of the GUI
        """

        assert isinstance(master, Tk), "'master' must be an instance of Tk"

        Frame.__init__(self, master)
        master.minsize(width=800, height=640)
        self.grid()
        self.canvas = Canvas(self, width=640, height=640)
        self.canvas.grid(row=0, column=0)
        self.sizeSquare = 80
        self.offsetPiece = 20

    def createChecker(self, x, y):
        """
            Create the GUI of a checker

            Arguments
            ----------
            x: int
                the absiss of the checker
            y: int
                the ordinate of the checker
            
            Return
            ----------
            int: the id of the checker in the canvas
        """

        assert type(x) is int and x >= 0, "'x' must be an integer greater than 0"
        assert type(y) is int and y >= 0, "'y' must be an integer greater than 0"

        return self.canvas.create_oval(x*self.sizeSquare + self.offsetPiece, y*self.sizeSquare + self.offsetPiece, (x+1)*self.sizeSquare - self.offsetPiece, (y+1)*self.sizeSquare - self.offsetPiece)
    
    def createSquare(self, x, y):
        """
            Create the GUI of a square

            Arguments
            ----------
            x: int
                the absiss of the square
            y: int
                the ordinate of the square
            
            Return
            ----------
            int: the id of the checker in the canvas
        """

        assert type(x) is int and x >= 0, "'x' must be an integer greater than 0"
        assert type(y) is int and y >= 0, "'y' must be an integer greater than 0"

        return self.canvas.create_rectangle(x*self.sizeSquare, y*self.sizeSquare, (x+1)*self.sizeSquare, (y+1)*self.sizeSquare)
    
    def colorObject(self, item, color):
        """
            Color an object

            Arguments
            ----------
            item: int
                the id of the object
            color: string
                the color of the object
        """

        assert type(item) is int, "'item' must be an integer"
        assert type(color) is str, "'color' must be a string"

        self.canvas.itemconfigure(item, fill=color)

    def moveChecker(self, item, x, y):
        """
            Move a checker

            Arguments
            ----------
            item: int
                the id of the checker moved
            x: int
                the absiss of the square
            y: int
                the ordinate of the square
        """

        assert type(x) is int and x >= 0, "'x' must be an integer greater than 0"
        assert type(y) is int and y >= 0, "'y' must be an integer greater than 0"

        self.canvas.coords(item, x*self.sizeSquare + self.offsetPiece, y*self.sizeSquare + self.offsetPiece, (x+1)*self.sizeSquare - self.offsetPiece, (y+1)*self.sizeSquare - self.offsetPiece)
    
    def killChecker(self, item):
        """
            Kill a checker

            Arguments
            ----------
            item: int
                the id of the checker killed
        """

        assert type(item) is int, "'item' must be an integer"

        self.canvas.delete(item)
    
    def changeIntoKing(self, item, x, y, color):
        """
            Change a checker in a king

            Arguments
            ----------
            item: int
                the id of the checker to change
            x: int
                the absiss of the square
            y: int
                the ordinate of the square
            color: str
                the color of the square
            
            Return
            ----------
            int: the new id of the checker changed in the canvas
        """

        assert type(x) is int and x >= 0, "'x' must be an integer greater than 0"
        assert type(y) is int and y >= 0, "'y' must be an integer greater than 0"
        assert type(item) is int, "'item' must be an integer"
        assert type(color) is str, "'color' must be a string"

        self.canvas.delete(item)
        new_item = self.canvas.create_rectangle(x*self.sizeSquare + self.offsetPiece, y*self.sizeSquare + self.offsetPiece, (x+1)*self.sizeSquare - self.offsetPiece, (y+1)*self.sizeSquare - self.offsetPiece)
        self.colorObject(new_item, color)
        return new_item
