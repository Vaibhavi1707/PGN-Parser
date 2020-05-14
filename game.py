#from pieceMoveModule import *
import validateMoves as vm
import re

def setup():
    squares = [x + y for x in 'ABCDEFGH' for y in '12345678']
    pieces = 'RNBQKBNR' + 'P' * 8 + '_' * 32 + 'p' * 8 + 'rnbqkbnr'
    boardview = dict(zip(squares, pieces))
    pieceview = {_: [] for _ in 'RNBPQKBNRrnbpqkbnr'}
    for sq in squares:
        piece = boardview[sq]
        if piece != '_':
            pieceview[piece].append(sq)
    return boardview, pieceview

def pgnToMoves(gameFile):
    raw_pgn = ' '.join([line.strip() for line in open(gameFile)])
    comments_marked = raw_pgn.replace('{', '<').replace('}', '>')
    STRC = re.compile('<[^>]*>')
    comments_removed = STRC.sub(' ', comments_marked)
    STR_marked = comments_removed.replace('[', '<').replace(']', '>')
    str_removed = STRC.sub(' ', STR_marked)
    MOVE_NUM = re.compile('[1-9][0-9]* *\.')
    just_moves = [_.strip() for _ in MOVE_NUM.split(str_removed)]
    print(just_moves)
    last_move = just_moves[-1]
    RESULT = re.compile("( *1 *- *0 *| *0 *- *1 *| *1/2 *- *1/2 *)")
    last_move = RESULT.sub('', last_move)
    moves = just_moves[:-1] + [last_move]
    
    return [_ for _ in moves if len(_) > 0]

def pre_process_move(board, piece_view, move):
    wmove, bmove = move.split()
    if wmove[0] in 'abcdefgh':
        wmove = 'P' + wmove
    if bmove[0] in 'abcdefgh':
        bmove = 'p' + bmove
    else:
        bmove = bmove.lower()
    return wmove, bmove

def pre_process_moves(board, piece_view, moves):
    return [pre_process_move(board, piece_view, move) for move in moves]

def display(board, i):
    return '_|'.join(board[pos] for pos in [x + y for x in 'ABCDEFGH' for y in '12345678'][(8 * i - 8):(8 * i)])

def capture(extra):
    return 'x' in extra

def update_captured_piece(piece_view, captured_piece, dest):
    piece_view[captured_piece].remove(dest.upper())

def make_capture_move(board, piece_view, dest, color, init_pos = None):
    captured_piece = board[dest.upper()]
    make_normal_move(board, piece_view, color, dest, init_pos)
    update_captured_piece(piece_view, captured_piece, dest) 

def make_normal_move(piece, board, piece_view, color, dest, given_init_pos = None):
    possible_pos = piece_view[piece.upper() if color == 'white' else piece.lower()]
    if given_init_pos :
        possible_pos[possible_pos.index(given_init_pos)] = dest.upper()
        board[dest.upper()] = piece.upper() if color == 'white' else piece.lower()
        board[given_initial_pos.upper()] = '_'
        return
    
    for pos, init_pos in enumerate(possible_pos):
        if vm.validPlace(color, piece, init_pos, dest):
            possible_pos[pos] = dest.upper()
            board[dest.upper()] = piece.upper() if color == 'white' else piece.lower()
            board[init_pos.upper()] = '_'
            return

def promotion(move):
    return '=' in move

def make_promotion(move):
    piece, dest, promoted_to = move[0], move[1:3], move[-1]
    init_pos = dest[0]+'7' if piece.isupper() else dest[0]+'2'
    piece_view[promoted_to].append(dest)
    piece_view[piece].remove(init_pos)
    board[dest] = promoted_to

def make_pawn_move(board, piece_view, color, extra, dest, move):
    if capture(extra, dest):
        make_capture_pawn_move(board, piece_view, dest, color)
    elif promotion(move):
        make_promotion(move)
    else:
        make_normal_pawn_move('p', board, piece_view, color, dest)

def pawn_move(piece):
    return piece.lower() == 'p'

def castling(move):
    return 'O' in move.upper()

def make_move(board, piece_view, color, move):
    piece, extra, dest = move[0], move[1: -2], move[-2:]
    
    if pawn_move(piece):
        make_pawn_move(board, piece_view, color, extra, dest, move)
    
    else:
        init_pos = ''
        if len(extra) >= 2:
            for i in '12345678': 
                if board[extra[0] + i] == piece:
                    init_pos = extra[0] + i
                    break
        if castling(move):
            do_castling(board, piece_view)
        elif capture(extra):
            make_capture(board, piece_view, dest, color, init_pos)
        else:
            make_normal_move(piece, board, piece_view, color, dest, init_pos)

def update_board(board, piece_view, moves):
    for move in moves:
        wmove, bmove = move
        make_move(board, piece_view, 'white', wmove)
        make_move(board, piece_view, 'black', bmove)
        for i in range(9):
            print(display(board, i))
        break

moves = pgnToMoves('pgn01.txt')
board, piece_view = setup()
processed_moves = pre_process_moves(board, piece_view, moves)
update_board(board, piece_view, processed_moves)