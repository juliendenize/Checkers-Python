class Square:
    """
        Represent a checker object

        Attributes
        ----------
        x : int
             Absciss
        y : int
            ordinate
        checker: @Checker
        color : string
            color of the checker
        ui : int
            id of the checker for the board canvas
    """

    def __init__(self, x, y, ui):
        """
            Construct the Square object

            Parameters
            ----------
            x : int
                absciss
            y : int
                ordinate
            ui : int
                the ui id
        """
        self.x = x
        self.y = y
        self.checker = None
        self.color = "#000000" if (x + y) % 2 else "#FA6565"
        self.ui = ui    
    
    def setChecker(self, checker):
        """
            Represent a checker object
            
            Arguments
            ----------
            checker : Checker
                the checker on the square
        """

        self.checker = checker