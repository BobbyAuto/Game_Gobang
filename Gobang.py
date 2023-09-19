import numpy as np
class Gobang:
    def __init__(self, ROWS, COLS, searchingDepth):
        self.ROWS = ROWS
        self.COLS = COLS
        self.Human = "H"            # represents Human chess pieces on the border
        self.Computer = "C"         # represents Computer chess pieces on the border
        self.EMPTY = " "            # represents no chess piece in the current position on the border
        self.searchingDepth = searchingDepth
        self.board = np.full((self.ROWS, self.COLS), self.EMPTY, dtype=str)

        self.results = None
        self.resetResults();

    def resetResults(self):
        """
        reset the results to go to next round
        :return:
        """
        self.results = np.full((self.ROWS, self.COLS), -2)


    def printBoard(self):
        """
        visualize the current board.
        :return:
        """
        str = "";
        for row in self.board:
            for e in row:
                if e == self.Human or e == self.Computer:
                    str += (e + "  ")
                else:
                    str += ('0  ' + e)
            print(str)
            str = "";
        print()



gobang = Gobang(8, 8, 4)
print(gobang.printBoard())