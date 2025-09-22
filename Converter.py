import torch

PIECE_PLANES = {
    'Pawn': 0,
    'Knight': 1,
    'Bishop': 2,
    'Rook': 3,
    'Queen': 4,
    'King': 5
}


def structured_games_to_tensor_batch(structured_games, side_to_moves=None, graveyard_coord=(100, 100)):
    """
    Convert transposed structured games into (N, 8, 8, 17) tensor batch.

    structured_games:
    [
       [white_pieces_game1, white_pieces_game2, ...],
       [black_pieces_game1, black_pieces_game2, ...],
       [wk1, wk2, ...],
       [wq1, wq2, ...],
       [bk1, bk2, ...],
       [bq1, bq2, ...]
    ]

    side_to_moves (optional): list of 0/1 values for each game.
    graveyard_coord: coordinate representing a captured piece; these are ignored on the board.
    """
    white_pieces_list = structured_games[0]
    black_pieces_list = structured_games[1]
    wk_list = structured_games[2]
    wq_list = structured_games[3]
    bk_list = structured_games[4]
    bq_list = structured_games[5]

    num_games = len(white_pieces_list)
    batch = []

    for i in range(num_games):
        tensor = torch.zeros((8, 8, 17), dtype=torch.float32)

        # White pieces
        for piece, (x, y) in white_pieces_list[i]:
            if (x, y) != graveyard_coord:
                tensor[y - 1, x - 1, PIECE_PLANES[piece]] = 1.0

        # Black pieces
        for piece, (x, y) in black_pieces_list[i]:
            if (x, y) != graveyard_coord:
                tensor[y - 1, x - 1, 6 + PIECE_PLANES[piece]] = 1.0

        # Castling
        tensor[:, :, 12] = wk_list[i]
        tensor[:, :, 13] = wq_list[i]
        tensor[:, :, 14] = bk_list[i]
        tensor[:, :, 15] = bq_list[i]

        # Side to move (plane 16), if provided
        if side_to_moves is not None:
            tensor[:, :, 16] = 1.0 if side_to_moves[i] == 1 else 0.0

        batch.append(tensor)

    return torch.stack(batch)  # Shape (N, 8, 8, 17)



import torch

PIECE_PLANES = {
    'Pawn':   0,
    'Knight': 1,
    'Bishop': 2,
    'Rook':   3,
    'Queen':  4,
    'King':   5
}
INV_PIECE_PLANES = {v: k for k, v in PIECE_PLANES.items()}


def tensor_to_pretty_board(tensor):
    """
    Convert a single (8,8,17) tensor into a human-readable board string.
    """
    board = [["." for _ in range(8)] for _ in range(8)]

    # White pieces: planes 0–5
    for piece_idx in range(6):
        coords = (tensor[:, :, piece_idx] == 1).nonzero(as_tuple=False)
        for y, x in coords:
            piece = INV_PIECE_PLANES[piece_idx][0]  # letter
            board[7-y][x] = piece.upper()           # white uppercase

    # Black pieces: planes 6–11
    for piece_idx in range(6):
        coords = (tensor[:, :, 6+piece_idx] == 1).nonzero(as_tuple=False)
        for y, x in coords:
            piece = INV_PIECE_PLANES[piece_idx][0]
            board[7-y][x] = piece.lower()           # black lowercase

    # Convert rows to strings
    rows = [" ".join(rank) for rank in board]

    # Extra info: castling + side to move
    wk = int(tensor[0, 0, 12].item())
    wq = int(tensor[0, 0, 13].item())
    bk = int(tensor[0, 0, 14].item())
    bq = int(tensor[0, 0, 15].item())
    stm = "White" if tensor[0, 0, 16].item() == 1 else "Black"

    castling = ""
    if wk: castling += "K"
    if wq: castling += "Q"
    if bk: castling += "k"
    if bq: castling += "q"
    if castling == "": castling = "-"

    return "\n".join(rows) + f"\n[{stm} to move, Castling: {castling}]"


def batch_to_pretty_boards(batch_tensor):
    """
    Pretty-print all boards in a batch tensor of shape (N, 8, 8, 17).
    """
    outputs = []
    for i in range(batch_tensor.shape[0]):
        board_str = tensor_to_pretty_board(batch_tensor[i])
        outputs.append(f"Game {i+1}:\n{board_str}")
    return "\n\n".join(outputs)




PIECE_PLANES = {
    'Pawn':   0,
    'Knight': 1,
    'Bishop': 2,
    'Rook':   3,
    'Queen':  4,
    'King':   5
}
INV_PIECE_PLANES = {v: k for k, v in PIECE_PLANES.items()}

# Expected counts per piece
EXPECTED_COUNTS = {
    'Pawn': 8,
    'Knight': 2,
    'Bishop': 2,
    'Rook': 2,
    'Queen': 1,
    'King': 1
}


def batch_tensor_to_tuples(batch_tensor):
    """
    Convert a batch tensor (N, 8, 8, 17) back into the structured tuple format.
    Missing pieces are filled with (100,100).
    """
    N = batch_tensor.shape[0]

    all_white_pieces = []
    all_black_pieces = []
    all_wk, all_wq, all_bk, all_bq = [], [], [], []

    for i in range(N):
        tensor = batch_tensor[i]

        white_pieces = []
        black_pieces = []

        # --- White pieces (planes 0–5) ---
        for piece_name, piece_idx in PIECE_PLANES.items():
            coords = (tensor[:, :, piece_idx] == 1).nonzero(as_tuple=False)
            coords_list = [(x.item()+1, y.item()+1) for y, x in coords]

            # Pad with (100,100) if fewer than expected
            while len(coords_list) < EXPECTED_COUNTS[piece_name]:
                coords_list.append((100, 100))

            # If too many (shouldn’t happen in chess), trim
            coords_list = coords_list[:EXPECTED_COUNTS[piece_name]]

            for coord in coords_list:
                white_pieces.append((piece_name, coord))

        # --- Black pieces (planes 6–11) ---
        for piece_name, piece_idx in PIECE_PLANES.items():
            coords = (tensor[:, :, 6+piece_idx] == 1).nonzero(as_tuple=False)
            coords_list = [(x.item()+1, y.item()+1) for y, x in coords]

            while len(coords_list) < EXPECTED_COUNTS[piece_name]:
                coords_list.append((100, 100))

            coords_list = coords_list[:EXPECTED_COUNTS[piece_name]]

            for coord in coords_list:
                black_pieces.append((piece_name, coord))

        all_white_pieces.append(white_pieces)
        all_black_pieces.append(black_pieces)

        # --- Castling rights ---
        all_wk.append(int(tensor[0, 0, 12].item()))
        all_wq.append(int(tensor[0, 0, 13].item()))
        all_bk.append(int(tensor[0, 0, 14].item()))
        all_bq.append(int(tensor[0, 0, 15].item()))

    return [
        all_white_pieces,
        all_black_pieces,
        all_wk,
        all_wq,
        all_bk,
        all_bq
    ]
x = structured_games_to_tensor_batch([[[('Pawn', (1, 2)), ('Pawn', (2, 3)), ('Pawn', (3, 2)), ('Pawn', (4, 2)), ('Pawn', (5, 2)), ('Pawn', (6, 2)), ('Pawn', (7, 2)), ('Pawn', (8, 2)), ('Rook', (1, 1)), ('Knight', (2, 1)), ('Bishop', (3, 1)), ('Queen', (4, 1)), ('King', (5, 1)), ('Bishop', (6, 1)), ('Knight', (7, 1)), ('Rook', (8, 1))]], [[('Pawn', (1, 7)), ('Pawn', (2, 7)), ('Pawn', (3, 7)), ('Pawn', (4, 7)), ('Pawn', (5, 7)), ('Pawn', (6, 7)), ('Pawn', (7, 7)), ('Pawn', (8, 7)), ('Rook', (1, 8)), ('Knight', (2, 8)), ('Bishop', (3, 8)), ('Queen', (4, 8)), ('King', (5, 8)), ('Bishop', (6, 8)), ('Knight', (7, 8)), ('Rook', (8, 8))]], [0], [0], [0], [0]]
)
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

board = tensor_to_chess_board(x[0], 'w')


 # e2e4, g1f3, etc.



def get_legal_move_destinations(board):
    """
    Returns legal moves in human-readable form:
    - "a3" for normal move
    - "xa6" for capture
    - "b4 check" if the move gives check
    - "xg6 check" if capture + check
    - "Castle King" or "Castle Queen" if that castling is currently legal
    """
    moves_output = []

    for move in board.legal_moves:
        # Castling moves
        if board.is_kingside_castling(move):
            moves_output.append("Castle King")
            continue
        if board.is_queenside_castling(move):
            moves_output.append("Castle Queen")
            continue

        # Normal moves
        to_square = chess.square_name(move.to_square)

        move_str = to_square

        # Capture?
        if board.is_capture(move):
            move_str = "x" + to_square

        # Check?
        temp_board = board.copy()
        temp_board.push(move)
        if temp_board.is_check():
            move_str += " check"

        moves_output.append(move_str)


    return moves_output



def legal_moves(game_state):

    statesforchess = []

    for i in range(len(game_state[0])):
        x = []
        x.append(game_state[0][i])
        x.append(game_state[1][i])
        x.append(game_state[2][i])
        x.append(game_state[3][i])
        x.append(game_state[4][i])
        x.append(game_state[5][i])
        statesforchess.append(x)

    states2 = []
    for y in statesforchess:
        states2.append(list_to_chess_board(y, turn='w'))


    g = []
    for x in states2:
        for i in get_legal_move_destinations(x):
            g.append(i)
    g = list(set(g))
    return(g)

game_state = [[[('Pawn', (1, 2)), ('Pawn', (2, 2)), ('Pawn', (3, 2)), ('Pawn', (4, 2)), ('Pawn', (5, 2)), ('Pawn', (6, 2)), ('Pawn', (7, 2)), ('Pawn', (8, 2)), ('Rook', (1, 1)), ('Knight', (1, 3)), ('Bishop', (3, 1)), ('Queen', (4, 1)), ('King', (5, 1)), ('Bishop', (6, 1)), ('Knight', (7, 1)), ('Rook', (8, 1))], [('Pawn', (1, 3)), ('Pawn', (2, 2)), ('Pawn', (3, 2)), ('Pawn', (4, 2)), ('Pawn', (5, 2)), ('Pawn', (6, 2)), ('Pawn', (7, 2)), ('Pawn', (8, 2)), ('Rook', (1, 1)), ('Knight', (2, 1)), ('Bishop', (3, 1)), ('Queen', (4, 1)), ('King', (5, 1)), ('Bishop', (6, 1)), ('Knight', (7, 1)), ('Rook', (8, 1))]], [[('Pawn', (1, 7)), ('Pawn', (2, 7)), ('Pawn', (3, 7)), ('Pawn', (4, 7)), ('Pawn', (5, 7)), ('Pawn', (6, 7)), ('Pawn', (7, 7)), ('Pawn', (8, 7)), ('Rook', (1, 8)), ('Knight', (2, 8)), ('Bishop', (3, 8)), ('Queen', (4, 8)), ('King', (5, 8)), ('Bishop', (6, 8)), ('Knight', (7, 8)), ('Rook', (8, 8))], [('Pawn', (1, 7)), ('Pawn', (2, 7)), ('Pawn', (3, 7)), ('Pawn', (4, 7)), ('Pawn', (5, 7)), ('Pawn', (6, 7)), ('Pawn', (7, 7)), ('Pawn', (8, 7)), ('Rook', (1, 8)), ('Knight', (2, 8)), ('Bishop', (3, 8)), ('Queen', (4, 8)), ('King', (5, 8)), ('Bishop', (6, 8)), ('Knight', (7, 8)), ('Rook', (8, 8))]], [0, 0], [0, 0], [0, 0], [0, 0]]
