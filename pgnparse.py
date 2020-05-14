import re

def setup():
    squares = [x + y for x in 'ABCDEFGH' for y in '12345678']
    pieces = 'RNBQKBNR' + 'P' * 8 + ' ' * 32 + 'p' * 8 + 'rnbqkbnr'
    boardview = dict(zip(squares, pieces))
    pieceview = {_: [] for _ in 'RNBPQKBNRrnbpqkbnr'}
    for sq in squares:
        piece = boardview[sq]
        if piece != ' ':
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
    last_move = RESU.sub('', last_move)
    moves = just_moves[:-1] + [last_move]
    
    return [_ for _ in moves if len(_) > 0]

def preProcessAMove(move):
    wmove, bmove = move.split()
    if wmove[0] in 'abcdefgh':
        wmove = 'P' + wmove
    if bmove[0] in 'abcdefgh':
        bmove = 'p' + bmove
    else:
        bmove = bmove.lower()
    return wmove, bmove

def preProcessMoves(moves):
    return [preProcessAMove(move) for move in moves[:-1]]

board, pieceview = setup()
moves = preProcessMoves(pgnToMoves('pgn01.txt'))
print(moves)