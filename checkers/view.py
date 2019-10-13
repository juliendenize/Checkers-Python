from tkinter import Canvas, Frame, Tk, Label, Button
import top_controller

class FirstMenu(Frame):
    def __init__(self, controller):
        assert isinstance(controller, top_controller.Controller), "'controller' must be an instance of Controller"
        self.controller = controller
        super().__init__(self.controller.master)
        self.grid(row=0, column=0)

        self.text1 = Label(self, text="Welcome on this wonderful Checkers game", bg="red")
        self.text1.grid(row=0, rowspan=3, column=6, ipadx=5, ipady=5, pady=10)

        self.text2 = Label(self, text="You can choose different game types:")
        self.text2.grid(row=5, column=6, pady=40)

        self.button1 = Button(self, text="Player VS Player", command=lambda: self.startGame(0))
        self.button1.grid(row=10, column=1, columnspan=3)

        self.button2 = Button(self, text="Player VS AI", command=lambda: self.startGame(1))
        self.button2.grid(row=10, column=5, columnspan=3)

        self.button3 = Button(self, text="AI VS AI", command=lambda: self.startGame(2))
        self.button3.grid(row=10, column=9, columnspan=3)
        
    def startGame(self, gameType):
        self.destroy()
        self.controller.startGame(gameType)

class BoardView(Frame):
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
            canvas: Canvas
                Canvas to display the board
        """

        assert isinstance(master, Tk), "'master' must be an instance of master"
        self.master = master
        super().__init__(self.master)
        self.master = master
        self.grid()
        self.board = Canvas(self, width=640, height=640)
        self.board.grid(row=0, column=0)
        self.scores = Canvas(self, bg="brown")
        self.scores.grid(row=0, column=1, sticky="nesw")
        self.initScores()
        self.sizeSquare = 80
        self.offsetPiece = 20

    def initScores(self):
        self.namePlayer1 = Label(self.scores, text="Player 1", bg="white", fg="black")
        self.namePlayer1.grid(row=0, column = 1)

        self.numberCheckers1 = Label(self.scores, text="12 checkers standing", bg="white", fg="black")
        self.numberCheckers1.grid(row=1, column = 1)

        self.namePlayer2 = Label(self.scores, text="Player 2", bg="black", fg="white")
        self.namePlayer2.grid(row=6, column = 1)

        self.numberCheckers2 = Label(self.scores, text="12 checkers standing", bg="black", fg="white")
        self.numberCheckers2.grid(row=7, column = 1)

    def updateScores(self, checkers1, checkers2):
        self.numberCheckers1.config(text=str(checkers1) + "checkers standing")
        self.numberCheckers2.config(text=str(checkers2) + "checkers standing")

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

        assert type(
            x) is int and x >= 0, "'x' must be an integer greater than 0"
        assert type(
            y) is int and y >= 0, "'y' must be an integer greater than 0"

        return self.board.create_oval(x*self.sizeSquare + self.offsetPiece, y*self.sizeSquare + self.offsetPiece, (x+1)*self.sizeSquare - self.offsetPiece, (y+1)*self.sizeSquare - self.offsetPiece)

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

        assert type(
            x) is int and x >= 0, "'x' must be an integer greater than 0"
        assert type(
            y) is int and y >= 0, "'y' must be an integer greater than 0"

        return self.board.create_rectangle(x*self.sizeSquare, y*self.sizeSquare, (x+1)*self.sizeSquare, (y+1)*self.sizeSquare)

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

        self.board.itemconfigure(item, fill=color)

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

        assert type(
            x) is int and x >= 0, "'x' must be an integer greater than 0"
        assert type(
            y) is int and y >= 0, "'y' must be an integer greater than 0"

        self.board.coords(item, x*self.sizeSquare + self.offsetPiece, y*self.sizeSquare + self.offsetPiece,
                           (x+1)*self.sizeSquare - self.offsetPiece, (y+1)*self.sizeSquare - self.offsetPiece)

    def killChecker(self, item):
        """
            Kill a checker

            Arguments
            ----------
            item: int
                the id of the checker killed
        """

        assert type(item) is int, "'item' must be an integer"

        self.board.delete(item)

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

        assert type(
            x) is int and x >= 0, "'x' must be an integer greater than 0"
        assert type(
            y) is int and y >= 0, "'y' must be an integer greater than 0"
        assert type(item) is int, "'item' must be an integer"
        assert type(color) is str, "'color' must be a string"

        self.board.delete(item)
        new_item = self.board.create_rectangle(x*self.sizeSquare + self.offsetPiece, y*self.sizeSquare +
                                                self.offsetPiece, (x+1)*self.sizeSquare - self.offsetPiece, (y+1)*self.sizeSquare - self.offsetPiece)
        self.colorObject(new_item, color)
        return new_item