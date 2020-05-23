class Symbol:
    """Draw and style attributes class
    """
    def __init__(self):
        self.color = None
        self.size = None
        self.symbol = None



class PieceBase:
    """Base class of a piece
    """
    def __init__(self, name, symbol):
        self.name = name
        self.team = None
        self.field = None
        self.board = None

class King(PieceBase):
    def __init__(self):
        super().__init__("King", symbol="K") 
