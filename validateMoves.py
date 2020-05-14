import sys

board = [ ['01', '01', '01', '01', '01', '01', '01', 'kb'],
          ['01', 'bb', '01', 'rb', '01', '01', 'pb', '01'],
          ['pb', '01', '01', '01', '01', '01', '01', 'pb'],
          ['01', 'pb', '01', '01', 'qb', 'nw', '01', '01'],
          ['01', '01', '01', 'bb', 'pw', '01', '01', '01'],
          ['01', '01', '01', 'qw', '01', '01', '01', '01'],
          ['pw', '01', '01', '01', '01', '01', 'pw', 'pw'],
          ['01', 'bw', '01', 'rw', '01', '01', '01', 'kw'] ]

def validPlace(color, piece, init_place, final_place):
    files = dict(zip(list('abcdefgh'), range(8)))
    ranks = dict(zip(list('12345678'), range(8)[::-1]))
    f0, r0 = files[init_place[0].lower()], ranks[init_place[1]]
    f1, r1 = files[final_place[0].lower()], ranks[final_place[1]]
    name = piece

    '''if board[f1][r1][1] == color or (r1 == r0 and f1 == f0) :
        return False'''

    def pawn(color):
        '''if f1 == f0 + 1 and r1 == r0 + 1 and board[f1][r1][1] != color:
            return True''' 
        #print(r0, r1, f0, f1)
        #print(r0, r1, f0, f1)
        return(((f1 == f0 + 2 or f1 == f0 + 3) and r1 == r0) and color == 'white') or (((f0 == f1 + 2 or f0 == f1 + 3) and r1 == r0) and color == 'black')

    def rook():
        return r1 == r0 or f1 == f0

    def knight():
        return (abs(f1 - f0), abs(r1 - r0)) in [(1, 2), (2, 1)]

    def bishop():
        return r1 != r0 and f1 != f0

    def queen():
        return (r1 == r0 or f1 == f0) or (r1 != r0 and f1 != f0)

    def king():
        return (abs(f1 - f0), abs(r1 - r0)) == (1, 1)

    pieces = {'p': pawn, 'r': rook, 'n': knight, 'b': bishop, 'q': queen, 'k': king} 
    return pieces[name](color)

if __name__ == "__main__":
    print(validPlace('pw', 'a2', 'a3'))

'''
Given a pgn file, we need to represent it on the board, then check if the next move is valid, whether 
we can capture another piece, check for checkmate and castling and en passant? 

Represent
1. The entire chess board
2. the pieces of the chess board, both white and black separately
3. The captured pieces
4. Empty positions
5. Filled positons

Tasks
1. To check if the new position moved to is valid
2. To check if after moving, we are able to capture the piece of the opponent
3. To check for check-mate
4. To move the right piece at the right time, to protect the king and to capture the opponents pieces.
'''