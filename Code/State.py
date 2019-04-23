from enum import Enum

class State(Enum):
    """
        Represent a State object for checkers

        Extends
        ----------
        Enum

        Values
        ----------
        NORMAL:
            checker is no king and alive
        KING:
            checker is a king
        DEAD:
            checker is dead
    """
    NORMAL = 1
    KING = 2
    DEAD = 3