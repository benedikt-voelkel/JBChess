# Some utilities
import numpy as np

from jbchess.game.game import Square, PhysicalArea

def make_chess_board(n_fields=8):
    square_length = 80
    world_length = n_fields * square_length

    world_square = Square(world_length)
    world_square.boarder_size = 2
    world_square.boarder_color = "black"

    square1 = Square(square_length)
    square1.fill = True
    square1.fill_color = "black"
    square2 = Square(square_length)
    square2.fill = True
    squares = (square1, square2)

    world = PhysicalArea(world_square)
    coord_lower = -(world_length / 2) + square_length / 2
    coord_upper = (world_length / 2) - square_length / 2

    for i, y in enumerate(np.linspace(coord_lower, coord_upper, n_fields)):
        for j, x in enumerate(np.linspace(coord_lower, coord_upper, n_fields)):
            child = PhysicalArea(squares[(i+j)%2])
            child.translation = (x, y)
            world.add_child(child)

    return world




def place(pieces_class, board, team, *fields):
    pieces = [pieces_class() for _ in fields]
    for p, f in zip(pieces, fields):
        team.add(p)
        board.place_piece(p, f)
    return pieces






def draw_board(board):
    if board.dim > 2:
        print(f"Cannot yet draw board of dimension {board.dim}")
        return
    symbols = np.array([""] * (board.size**board.dim), dtype=object)
    for p in board.pieces:
        team = p.team.number if p.team else "0"
        symbols[p.field] = f"{p.symbol}({team})"
    empty = ["    "] * board.size
    symbols[symbols == ""] = "    "
    symbols = symbols.reshape(*[board.size]*board.dim)
    string = "\n  --------------------------------------------------------- \n"
    for i in range(symbols.shape[0] - 1, -1, -1):
        string += f"  | " + " | ".join(empty) + " |\n"
        string += f"{i+1} | " + " | ".join(symbols[i,...]) + " |\n"
        string += f"  | " + " | ".join(empty) + " |\n"
        string += "  --------------------------------------------------------- \n"
    string += "     a      b      c      d      e      f      g      h \n"
    print(string)
