# This is for now just an example implementation

import sys


class BoardBase:
    """Base class for anything which can be placed on the board

    BoardBase objects can be added, subtracted etc.
    ==> Operators to be overridden

    """
    def __init__(self, occupied=0, **kwargs):
        """Init chess boar

        Args:
            occupied: bits equal 1 indicate field is occupied
        """
        # 64-bit number with bits set to 1 for each field occupied
        self.occupied = occupied
        self.symbols = None

        self.symbol = kwargs.get("symbol", "x")


    def prepare_symbol_list(self):
        if not self.symbols:
            self.symbols = [None] * 64
        for i in range(64):
            if self.occupied & (1 << i):
                self.symbols[i] = self.symbol
                continue
            self.symbols[i] = None


    def __str__(self):
        self.prepare_symbol_list()
        string = ""
        for i, s in enumerate(self.symbols):
            if i % 8 == 0:
                string = string + "\n---------------------------------\n|"
            if s:
                string = string + f" {s} |"
                continue
            string = string + "   |"
        string = string + "\n---------------------------------\n"
        return string


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


class BoardCollection(BoardBase):
    """A collection of boards

    Can be used to merge boards of different pieces

    """

    def __init__(self, *boards):
        """Initialise with boards

        Collect all boards

        """
        super().__init__()
        self.boards = boards

        self.update_board()


    def check_sanity(self):
        """Quick sanity check for overlapping pieces
        """
        occupied_or = 0
        occupied_xor = 0

        # Same fields have to (not) be occupied by OR and XOR operation
        for b in self.boards:
            occupied_or = occupied_or | b.occupied
            occupied_xor = occupied_xor ^ b.occupied
            if occupied_or != occupied_xor:
                return False
        return True


    def update_board(self):
        """Update board
        """
        if not self.check_sanity():
            print("ERROR: Overlapping pieces")
            sys.exit(1)
        self.occupied = 0
        for b in self.boards:
            self.occupied = self.occupied | b.occupied


    def __str__(self):
        symbols = [None] * 64
        for b in self.boards:
            b.prepare_symbol_list()
            for i, s in enumerate(b.symbols):
                if s:
                    symbols[i] = s

        string = ""
        for i, s in enumerate(symbols):
            if i % 8 == 0:
                string = string + "\n---------------------------------\n|"
            if s:
                string = string + f" {s} |"
                continue
            string = string + "   |"
        string = string + "\n---------------------------------\n"
        return string
