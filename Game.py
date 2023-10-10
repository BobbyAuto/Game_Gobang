from Gobang import Gobang

size = 11
depth = 2
gobang = Gobang(size, depth)

''' create a board situations for classification 1. '''
# gobang.board[3, 5] = 255
# gobang.board[4, 4] = 255
# gobang.board[4, 5] = 255
# gobang.board[4, 6] = 0
# gobang.board[5, 4] = 255
# gobang.board[5, 5] = 255
# gobang.board[5, 6] = 0
# gobang.board[6, 4] = 255
# gobang.board[6, 5] = 0
# gobang.board[6, 6] = 0
# gobang.board[7, 4] = 0
# gobang.board[7, 6] = 0

''' create a board situations for classification 3. '''
# gobang.board[2, 5] = 0
#
# gobang.board[3, 5] = 255
# gobang.board[4, 5] = 255
# gobang.board[2, 4] = 255
#
# gobang.board[4, 4] = 255
#
# gobang.board[3, 4] = 0
# gobang.board[4, 3] = 0

''' create a board situations for classification 3-2. '''
# gobang.board[2, 5] = 0
#
# gobang.board[3, 5] = 255
# gobang.board[4, 5] = 255
# gobang.board[2, 4] = 255
#
# gobang.board[4, 4] = 255
#
# gobang.board[3, 4] = 0
# gobang.board[4, 3] = 0


''' create a board situations for classification 4. '''
# gobang.board[2, 5] = 0
#
# gobang.board[3, 6] = 255
# gobang.board[4, 6] = 255
# gobang.board[2, 4] = 255
#
# gobang.board[4, 4] = 255
#
# gobang.board[3, 4] = 0
# gobang.board[4, 5] = 0

gobang.start()