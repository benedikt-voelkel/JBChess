# This is for now just an example implementation

import sys
import numpy as np


class Move:
    def __init__(self, board, start, end):
        self.board = board
        self.start = start
        self.end = end


    def __str__(self):
        return f"Board {self.board.name} from {self.start} to {self.end}"

class History:
    def __init__(self):

        # The current history
        self.history = []
        # Past histories (kept e.g. in case something was reverted)
        self.past_histories = []

    def add(self, move):
        self.history.append(move)

    def revert(self):
        if history:
            for h in history:
                self.past_histories.append([h for h in history])
            history.pop()


    def __str__(self):
        _str = "######## This is the history: #########\n"
        for i, h in enumerate(self.history):
            _str += f"Move {i}: {h}\n"
        _str += "#######################################\n"
        return _str


class RuleBase:
    def __init__(self, name):
        self.name = name

    def check(self, move, full_history, full_board):
        return True


class RuleDontHitSameTeam(RuleBase):
    def __init__(self):
        super().__init__("DontHitSameTeam")


    def check(self, move, full_history, board):
        if move.board.collection and move.board.collection.occupied & move.end:
            return False
        return True




class Team:
    def __init__(self, name):
        self.name = name
        self.pieces = []
        self.number = 0

    def add(self, piece):
        self.pieces.append(piece)
        piece.team = self


class Board:
    """A board
    """

    def __init__(self, name, size=8, dim=2):

        self.size = size
        self.dim = dim
        self.board_dummy = np.array([None] * (size**dim), dtype=object)
        self.teams = []
        self.pieces = []
        self.closed = False

        # Update the boards self.occupied member from collected boards
        self.rules = [RuleDontHitSameTeam()]
    
    
    def add_team(self, piece):
        if piece.team and piece.team not in self.teams:
            self.teams.append(piece.team)

    def add_piece(self, piece):
        self.pieces.append(piece)

    def place_piece(self, piece, field):
        if not piece.team:
            print(f"Piece {piece.name} has no team")
            sys.exit(1)
        if field < 0 or field > len(self.board_dummy):
            print(f"Field {field} does not exist in board {board.name}")
            sys.exit(1)
        if self.board_dummy[field]:
            print(f"There is already a piece on field {field}")
            sys.exit(1)
        self.add_team(piece)
        self.add_piece(piece)
        self.board_dummy[field] = piece
        piece.field = field
        print(f"Added piece {piece.name} for team {piece.team.name}")


    def check_ready(self):
        if not self.pieces:
            print("There are no pieces on board {self.name}")
            return False
        if not self.teams:
            print("There are no teams on board {self.name}")
            return False
        pieces_no_team = []
        for p in self.pieces:
            if not p.team:
                pieces_no_team.append(p)
        if pieces_no_team:
            print("There are pieces without a team")
            return False
        return True


    def close(self):
        if self.closed:
            print(f"Board {self.name} already closed")
            return
        if not self.check_ready():
            print(f"Cannot close board")
            sys.exit(1)

        for i, t in enumerate(self.teams):
            t.number = i + 1
        
        self.closed = True


    def possible_move(self, start, end):
        if not self.occupied & start:
            print(f"ERROR: No piece at {start}")
            return False
        return self.find_board(start).possible_move(start_end)



    def check_move(self, start, end):
        """Check whether a move is possible hypothetically
        """
        board = self.find_board(start)
        if not board:
            print(f"ERROR: There is no piece at {start}")
            return False, self
        move = Move(board, start, end)
        for r in self.rules:
            if not r.check(move, self.history, self):
                print(f"Cannot move according to rule {r.name}")
                return False, self
        if not self.occupied & end:
            # Target field is free, so good to go
            return True, board


    def move(self, start, end):
        possible, board = self.check_move(start, end)
        if possible:
            board.occupied += end
            board.occupied -= 1
            self.update_board()
            self.add_move(board, start, end)

    def add_move(self, board, start, end):
        move = Move(board, start, end)
        self.history.add(move)
        board.history.add(move)


class RuleCannotJump:
    def __init__(self):
        super().__init__("CannotJump")


def compute_straight(start, template_cube, axis=-1, bound=None):
    """Compute straight lines in cube
    
    Args:
        start: int
            start coordinate
        axis: int
            axis to compute straight line on
        dim: int
            number of cube dimensions
        length: int
            length of one cube dimensions
        bound: iterable
            relative maximum boundaries
    """ 
    dim = len(template_cube.shape)
    length = template_cube.shape[0]
    if len(start) != dim:
        print(f"Starting point needs to have dimension {dim}")
        return (-1) * dim

    if axis == -1:
        axis = [d for d in range(dim)]

    for a in axis:
        if a >= dim:
            print(f"Have only {dim} dimensions but axis {a} was requested")
            return (-1) * dim

    reach = []
    for a in axis:
        new_start = list(start).copy()
        new_start[a] = 0
        for l in range(length):
            next_reach = new_start.copy()
            next_reach[a] = l
            reach.append(next_reach)
    return reach


class MoveBase:
    def __init__(self, name):
        self.name = name

    def end_positions(self, start, full_history, full_board):
        return [0] * len(full_board.occupied.shape)

class MoveTower(MoveBase):
    def __init__(self):
        super().__init__("MoveTower")
        self.rules = [RuleDontHitSameTeam()]

    def end_positions(self, start, full_history, full_board):
        ends = compute_straight(start)




