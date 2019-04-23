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
            the checker hold by the square
        color : string
            color of the square
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
