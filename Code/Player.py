class Player:
    """
        Represent a player object

        Attributes
        ----------
        name: string
            the name of the player
        id: int
                the id of the player (0 or 1)
        time: Time
            the time the player played
        checkerNb: int
            the number of checkers alive
        mustAttack: int
            -1 if the player can't move, 0 if the player can't jump, 1 if he can jump, 2 if he can jump and already jumped
        lastNormalPieceMovedMoves: int
            number of moves since the player didn't move a normal piece
        lastJumpMoves: int
            number of moves since the player didn't jump
    """

    def __init__(self, name, id):
        """
            Construct the player object

            Parameters
            ----------
            name: string
                the name of the player
            id: int
                the id of the player (0 or 1)
        """
        self.name = name
        self.time = 0
        self.id = id
        self.checkerNb = 0
        self.mustAttack = 0
        self.lastNormalPieceMovedMoves = 0
        self.lastJumpMoves = 0