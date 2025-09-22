import chess
import Converter

import chess
import torch

PIECE_PLANES = {
    'Pawn': 0,
    'Knight': 1,
    'Bishop': 2,
    'Rook': 3,
    'Queen': 4,
    'King': 5
}

PIECE_SYMBOLS = {
    'Pawn': 'P',
    'Knight': 'N',
    'Bishop': 'B',
    'Rook': 'R',
    'Queen': 'Q',
    'King': 'K'
}


def list_to_chess_board(state_list, turn='w'):
    """
    Convert your tuple/list representation into a python-chess Board.

    state_list = [
        white_pieces,  # list of (piece_name, (x,y))
        black_pieces,  # list of (piece_name, (x,y))
        wk, wq, bk, bq # castling rights (0/1)
    ]
    turn = 'w' or 'b'
    """
    board = chess.Board(fen=None)
    board.clear()  # empty board

    white_pieces, black_pieces, wk, wq, bk, bq = state_list

    # Place white pieces
    for piece, (x, y) in white_pieces:
        if (x, y) == (100, 100):  # captured piece
            continue
        square = chess.square(x - 1, y - 1)
        board.set_piece_at(square, chess.Piece.from_symbol(PIECE_SYMBOLS[piece].upper()))

    # Place black pieces
    for piece, (x, y) in black_pieces:
        if (x, y) == (100, 100):
            continue
        square = chess.square(x - 1, y - 1)
        board.set_piece_at(square, chess.Piece.from_symbol(PIECE_SYMBOLS[piece].lower()))

    # Castling rights
    castling_rights = 0
    if wk: castling_rights |= chess.BB_H1  # White kingside (H1)
    if wq: castling_rights |= chess.BB_A1  # White queenside (A1)
    if bk: castling_rights |= chess.BB_H8  # Black kingside (H8)
    if bq: castling_rights |= chess.BB_A8  # Black queenside (A8)
    # Instead of BB, python-chess uses board.castling_rights assignment:
    rights = ''
    if wk: rights += 'K'
    if wq: rights += 'Q'
    if bk: rights += 'k'
    if bq: rights += 'q'
    board.set_castling_fen(rights if rights else '-')

    # Set turn
    board.turn = chess.WHITE if turn == 'w' else chess.BLACK

    return board


def tensor_to_chess_board(tensor, turn='w', graveyard_coord=(100, 100)):
    """
    Convert an (8,8,17) tensor to a python-chess Board.
    """
    # Create empty state_list
    white_pieces, black_pieces = [], []

    for piece_name, idx in PIECE_PLANES.items():
        coords = (tensor[:, :, idx] == 1).nonzero(as_tuple=False)
        for y, x in coords:
            white_pieces.append((piece_name, (x.item() + 1, y.item() + 1)))

        coords_black = (tensor[:, :, 6 + idx] == 1).nonzero(as_tuple=False)
        for y, x in coords_black:
            black_pieces.append((piece_name, (x.item() + 1, y.item() + 1)))

    # Castling
    wk = int(tensor[0, 0, 12].item())
    wq = int(tensor[0, 0, 13].item())
    bk = int(tensor[0, 0, 14].item())
    bq = int(tensor[0, 0, 15].item())

    state_list = [white_pieces, black_pieces, wk, wq, bk, bq]

    return list_to_chess_board(state_list, turn=turn)

board = tensor_to_chess_board(tensor([[[[0., 0., 0.,  ..., 0., 0., 0.],
          [0., 1., 0.,  ..., 0., 0., 0.],
          [0., 0., 1.,  ..., 0., 0., 0.],
          ...,
          [0., 0., 1.,  ..., 0., 0., 0.],
          [0., 1., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.]],

         [[1., 0., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.],
          [1., 0., 0.,  ..., 0., 0., 0.],
          ...,
          [1., 0., 0.,  ..., 0., 0., 0.],
          [1., 0., 0.,  ..., 0., 0., 0.],
          [1., 0., 0.,  ..., 0., 0., 0.]],

         [[0., 0., 0.,  ..., 0., 0., 0.],
          [1., 0., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.],
          ...,
          [0., 0., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.]],

         ...,

         [[0., 0., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.],
          ...,
          [0., 0., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.]],

         [[0., 0., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.],
          ...,
          [0., 0., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.]],

         [[0., 0., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.],
          ...,
          [0., 0., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.],
          [0., 0., 0.,  ..., 0., 0., 0.]]]]), turn)

board = chess.Board(tensor_to_chess_board())

# Generate all legal moves
legal_moves = list(board.legal_moves)

# Example: convert moves to your own index scheme
for move in legal_moves:
    print(move.uci())  # e2e4, g1f3, etc.