import string

NUM_RANKS = 8
NUM_FILES = 8
STARTING_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
WHITE = 'White'
BLACK = 'Black'
WHITE_TO_MOVE = 'w'
BLACK_TO_MOVE = 'b'
WHITE_KING = 'K'
BLACK_KING = 'k'
WHITE_QUEEN = 'Q'
BLACK_QUEEN = 'q'
WHITE_ROOK = 'R'
BLACK_ROOK = 'r'
WHITE_BISHOP = 'B'
BLACK_BISHOP = 'b'
WHITE_PAWN = 'P'
BLACK_PAWN = 'p'
WHITE_KNIGHT = 'N'
BLACK_KNIGHT = 'n'
MATRIX_OCCUPIED = 1
MATRIX_EMPTY = 0

def empty_board() -> [MATRIX_EMPTY]:
    return [MATRIX_EMPTY for x in range(NUM_FILES * NUM_RANKS)]

def split_ws(_string: str) -> [str]:
    return _string.split(' ')

def to_move(fen: str) -> str:
    return split_ws(fen)[1]

def flatten(_list: [any]) -> [any]:
    acc = []
    for x in _list:        
        if isinstance(x, list):        
            acc = acc + flatten(x)
            continue
        acc.append(x)        
    return acc

def filter(_list: [any], fn) -> [any]:
    return [x for x in _list if fn(x)]

def print_board(board_matrix: [int]):
    if not len(board_matrix):
        return
    print(board_matrix[:NUM_RANKS])
    print_board(board_matrix[NUM_RANKS:])


def is_int(val: str) -> bool:
    for digit in string.digits:
        if val is digit:
            return True
    return False

def get_board(fen: str) -> [str]:
    def mapfn(square):
        if is_int(square):
            return ['' for x in range(int(square))]
        return square

    ranks = [rank for rank in split_ws(fen)[0].split('/')]
    
    return flatten([mapfn(square) for rank in ranks for square in rank])

def get_pieces_matrix(board: [str], piece: str) -> [MATRIX_OCCUPIED | MATRIX_EMPTY]: 
    lambda_expr = lambda x: MATRIX_OCCUPIED if x is piece else MATRIX_EMPTY
    return [lambda_expr(square) for square in board]
    
def is_a_pawn(board_index: int) -> bool:
    return board_index % NUM_RANKS == 0
def is_h_pawn(board_index: int) -> bool:
    return board_index % NUM_RANKS == NUM_RANKS - 1

def get_rank(board_index: int) -> int:
    return board_index // NUM_FILES

def get_file(board_index: int) -> int:
    return board_index % NUM_RANKS

def get_pawn_captures(board_index: int, color: str) -> [int]:
    left_capture = (board_index - NUM_RANKS - 1) if color is WHITE else (board_index + NUM_RANKS - 1)
    right_capture = (board_index - NUM_RANKS + 1) if color is WHITE else (board_index + NUM_RANKS + 1)
    if is_a_pawn(board_index):
        return [right_capture]
    if is_h_pawn(board_index):
        return [left_capture]
    return [left_capture, right_capture]

def get_white_pawn_captures(board_index: int) -> [int]:    
    return get_pawn_captures(board_index, WHITE)

def get_black_pawn_captures(board_index: int) -> [int]:    
    return get_pawn_captures(board_index, BLACK)

def get_bishop_captures(board_index: int) -> [int]:
    _file = get_file(board_index)
    _rank = get_rank(board_index)
    def main_diag(index: int, _file: int, _list: [int] = []) -> [int]:
        print(_file)
        if index < 0 or _file == 0:
            return _list
        square = index - NUM_FILES - 1
        return main_diag(square, _file - 1, _list + [square])
    return main_diag(board_index, _file)
    # return [x for x in range(NUM_RANKS * NUM_FILES) if board_index % x is 0 or ]

def get_rook_captures(board_index: int) -> [int]:
    _file = get_file(board_index)
    _rank = get_rank(board_index)
    return [square for square in range(NUM_RANKS * NUM_FILES) if square % NUM_RANKS == _file or square // NUM_FILES == _rank]

PIECE_CAPTURES_FNS = {
    WHITE_PAWN: get_white_pawn_captures,
    BLACK_PAWN: get_black_pawn_captures,
    WHITE_ROOK: get_rook_captures,
    BLACK_ROOK: get_rook_captures,
    WHITE_BISHOP: get_bishop_captures,
    BLACK_BISHOP: get_bishop_captures,
}

def get_pieces_captures(piece_matrix: [MATRIX_OCCUPIED | MATRIX_EMPTY], piece: str) -> [MATRIX_OCCUPIED | MATRIX_EMPTY]:
    board = empty_board()
    capture_fn = PIECE_CAPTURES_FNS[piece]
    for index in range(NUM_FILES * NUM_RANKS):
        square = piece_matrix[index]
        if square is MATRIX_EMPTY:
            continue
        captures = capture_fn(index)
        for index in captures:
            board[index] = MATRIX_OCCUPIED
    return board

print_board(get_pieces_captures(get_pieces_matrix(get_board(STARTING_POSITION), WHITE_BISHOP), WHITE_BISHOP))


