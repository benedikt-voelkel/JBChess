# This is for now just an example implementation


class BoardBase:
    """Base class for anything which can be placed on the board

    BoardBase objects can be added, subtracted etc.
    ==> Operators to be overridden

    """
    def __init__(self, occupied=0):
        """Init chess boar

        Args:
            occupied: bits equal 1 indicate field is occupied
        """
        # 64-bit number with bits set to 1 for each field occupied
        self.occupied = occupied


class PiecesBase(BoardBase):
    """Base class for all types of chess pieces

    This defines e.g. how a chess piece type can be moved 
    """

    def __init__(self, name, occupied=0):
        """Init chess piece object

        Args:
            name: Some name given to this chess piece type
            occupied: bits equal 1 indicate field is occupieid, this is forwarded to the base class
        """
        super().__init__(occupied)
        self.name = name


    def find_moves(self):
        """Find all fields this piece could move
        """



