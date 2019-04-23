class Player:
    """
        Represent a player object

        Attributes
        ----------
        name: string
            the name of the player
        time: Time
            the time the player played
        checkerNb: int
            the number of checkers alive
    """

    def __init__(self, name):
        """
            Construct the player object

            Parameters
            ----------
            name : string
                the name of the player
        """
        self.name = name
        self.time = 0
        self.checkerNb = 0