import pygame


class Gobang:
    def __init__(self, size, depth):
        self.size = size  # board size, represents a (size X size) board.

        self.player = 0  # initialize black chess color to represent a human player.
        self.AI = 255  # initialize white chess color to represent AI player.

        self.padding = 60  # the padding space to the four sides of the border.
        self.crossSpace = 40  # the distance between the positions of each chess piece.
        self.boardLength = self.crossSpace * (self.size - 1) + self.padding * 2  # the length of border sides.
        self.depth = depth  # search depth of tree in each iteration.
        self.board = self.initBoard()  # record all position of chess pieces
        self.piecesTrace = []  # trace all placed chess pieces

        self.screen = None
        self.initWindow()

    def initBoard(self):
        """
        initialize all chess pieces, -1 represents empty position.
        :return:
        """
        initBoard = {}
        for x in range(self.size):
            for y in range(self.size):
                initBoard[(x, y)] = -1
        return initBoard

    def initWindow(self):
        """
        initial a board window
        :return:
        """
        pygame.init()
        pygame.display.set_caption('AI 60pts Project Assignment')  # the title of border
        self.screen = pygame.display.set_mode((self.boardLength, self.boardLength))
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255),
                         ((self.boardLength / 2, 0), (self.boardLength / 2, self.boardLength)), 0)

        font = pygame.font.Font(None, 36)  # set a font size
        text_surface = font.render("Click to choose your chess color.", True, (255, 0, 0))  # set a red text color
        text_surface_2 = font.render("Black or White", True, (255, 0, 0))  # set a red text color
        self.screen.blit(text_surface, (50, 100))
        self.screen.blit(text_surface_2, (150, 140))

        pygame.display.update()

        isColorChosen = False
        while isColorChosen is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Register a click event for chess color choosing
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()  # Obtain the coordinates of mouse clicks
                    isColorChosen = True
                    if x < self.boardLength / 2:  # player choose black piece color
                        self.AI = 255
                        self.player = 0
                    else:  # player choose white piece color
                        self.AI = 0
                        self.player = 255

    def start(self):
        """
        start the game
        :return: None
        """
        self.renderBoard()

        while True:
            for event in pygame.event.get():
                # quit the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # player round, obtain click event
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()  # Obtain the coordinates of mouse clicks
                    x = round((x - self.padding) / self.crossSpace)
                    y = round((y - self.padding) / self.crossSpace)
                    if 0 <= x < self.size and 0 <= y < self.size and self.board[(x, y)] == -1:
                        self.board[(x, y)] = self.player  # place a chess piece
                        self.piecesTrace.append((x, y))  # put the placed chess piece into a trace array
                        self.renderBoard()
                        self.checkWinner()

                        # it turns to AI round
                        pos = self.AIturn()
                        self.renderBoard(lastPiece=pos)
                        self.checkWinner()

                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_SPACE]:
                        print("K_Space!")
                        self.renderBoard()
                        continue
                    if len(self.piecesTrace) != 0:
                        self.board[self.piecesTrace[-1]] = -1
                    if len(self.piecesTrace) > 1:
                        self.board[self.piecesTrace[-2]] = -1
                        self.piecesTrace = self.piecesTrace[:-2]
                    self.renderBoard()

    def renderBoard(self, someoneWon=None, lastPiece=None):
        """
        render the board
        :param someoneWon: if AI or player win, then pass winner's information
        :param lastPiece: pass the last placed chess pieces to draw a reminder of last placed chess pieces.
        :return:
        """
        # draw background color
        self.screen.fill((150, 80, 0))

        # draw chess color reminder
        font = pygame.font.Font(None, 26)
        side_space = 30
        top_space = 30
        text_player = font.render("Player", True, (0, 0, 0))  # set a red text color
        self.screen.blit(text_player, (50, 22))
        pygame.draw.circle(self.screen, (self.player, self.player, self.player), (side_space, top_space), 10, 0)

        text_AI = font.render("AI", True, (0, 0, 0))  # set a red text color
        self.screen.blit(text_AI, (self.boardLength - side_space - 40, 22))
        pygame.draw.circle(self.screen, (self.AI, self.AI, self.AI), (self.boardLength - side_space, top_space), 10, 0)

        # draw chess mesh
        for x in range(0, self.crossSpace * self.size, self.crossSpace):
            pygame.draw.line(self.screen, (255, 255, 255), (x + self.padding, 0 + self.padding),
                             (x + self.padding, self.crossSpace * (self.size - 1) + self.padding), 1)
        for y in range(0, self.crossSpace * self.size, self.crossSpace):
            pygame.draw.line(self.screen, (255, 255, 255), (0 + self.padding, y + self.padding),
                             (self.crossSpace * (self.size - 1) + self.padding, y + self.padding), 1)
        # draw chess pieces
        for x in range(self.size):
            for y in range(self.size):
                color = self.board[(x, y)]
                if color != -1:
                    xi = self.padding + x * self.crossSpace
                    yi = self.padding + y * self.crossSpace
                    pygame.draw.circle(self.screen, (color, color, color), (xi, yi), 15, 0)

        # draw a reminder dot on the last chess piece which was placed by AI
        if lastPiece is not None:
            xi = self.padding + lastPiece[0] * self.crossSpace
            yi = self.padding + lastPiece[1] * self.crossSpace
            pygame.draw.circle(self.screen, (255, 0, 0), (xi, yi), 5, 0)

        # draw a win line and winer text.
        if someoneWon is not None:
            winPos = someoneWon["winPos"]
            pygame.draw.line(self.screen, (255, 0, 0),
                             (self.padding + self.crossSpace * winPos[0][0],
                              self.padding + self.crossSpace * winPos[0][1]),
                             (self.padding + self.crossSpace * winPos[1][0],
                              self.padding + self.crossSpace * winPos[1][1]), 5)
            font = pygame.font.Font(None, 66)
            text_player = font.render(someoneWon["winner"], True, (255, 0, 0))  # set a red text color
            self.screen.blit(text_player, (185, 25))

        pygame.display.update()

    def AIturn(self, ):
        """
        it turns to AI
        :return: the best position
        """
        score, _, position = self.minimax(self.board, self.depth, self.AI, float('-inf'), float('inf'))
        print('AI得分：', score)
        self.board[position] = self.AI
        self.piecesTrace.append(position)
        return position

    def minimax(self, board, dep, whoTurns, last_alpha, last_beta):
        """
        minimax algorithm
        :param board:
        :param dep:
        :param whoTurns:
        :param last_alpha:
        :param last_beta:
        :return:
        """
        if whoTurns == self.AI:  # if AI turns, maximize the payoff.
            return self.maxValue(board, dep, self.AI, last_alpha, last_beta)
        else:  # if player turns, minimize the payoff.
            return self.minValue(board, dep, self.player, last_alpha, last_beta)

    def maxValue(self, board, dep, color, last_alpha, last_beta):
        """
        maximize AI's payoff
        :param board:
        :param dep:
        :param color:
        :param last_alpha:
        :param last_beta:
        :return:
        """
        board_temp = board.copy()

        if dep == 0:
            score = self.evaluate(board_temp, self.AI) - self.evaluate(board_temp, self.player)
            return score, score, (-1, -1)

        alpha = float('-inf')
        beta = last_beta

        for x in range(self.size):
            for y in range(self.size):
                if self.skipCross(x, y):
                    continue
                if board_temp[(x, y)] == -1:
                    board_temp[(x, y)] = color
                    next_alpha, next_beta, _ = self.minValue(board_temp, dep - 1, self.player, alpha, beta)
                    board_temp[(x, y)] = -1
                    if alpha < next_beta:
                        alpha = next_beta
                        pos = (x, y)

                    if beta < alpha:  # alpha, beta pruning
                        return alpha, beta, pos
        return alpha, beta, pos

    def minValue(self, board, dep, color, last_alpha, last_beta):
        """
        minimize player's payoff
        :param board:
        :param dep:
        :param color:
        :param last_alpha:
        :param last_beta:
        :return:
        """
        board_temp = board.copy()

        if dep == 0:
            score = self.evaluate(board_temp, self.AI) - self.evaluate(board_temp, self.player)
            return score, score, (-1, -1)

        alpha = last_alpha
        beta = float('inf')

        for x in range(self.size):
            for y in range(self.size):
                if self.skipCross(x, y):
                    continue
                if board_temp[(x, y)] == -1:
                    board_temp[(x, y)] = color
                    next_alpha, next_beta, _ = self.maxValue(board_temp, dep - 1, self.AI, alpha, beta)
                    board_temp[(x, y)] = -1

                    if color == self.player and beta > next_alpha:
                        beta = next_alpha
                        pos = (x, y)
                    if beta < alpha:  # alpha, beta pruning
                        return alpha, beta, pos
        return alpha, beta, pos

    def skipCross(self, x, y):
        if x == 0 or y == 0 or x == self.size - 1 or y == self.size - 1:
            return False
        if self.board[(x - 1, y - 1)] == self.board[(x - 1, y)] == self.board[(x - 1, y + 1)] == \
                self.board[(x, y - 1)] == self.board[(x, y)] == self.board[(x, y + 1)] == \
                self.board[(x + 1, y - 1)] == self.board[(x + 1, y)] == self.board[(x + 1, y + 1)] == -1:
            return True
        return False

    def evaluate(self, board, color):
        """
        evaluate the situation, and return the evaluated score.
        :param board:
        :param color:
        :return:
        """
        score = 0
        # horizontal
        for x in range(self.size):
            for y in range(self.size - 5):
                score += self.getScore(color, (board[(x, y)], board[(x, y + 1)],
                                               board[(x, y + 2)], board[(x, y + 3)], board[(x, y + 4)],
                                               board[(x, y + 5)]))
        # vertical
        for x in range(self.size - 5):
            for y in range(self.size):
                score += self.getScore(color, (board[(x, y)], board[(x + 1, y)],
                                               board[(x + 2, y)], board[(x + 3, y)], board[(x + 4, y)],
                                               board[(x + 5, y)]))
        # diagonal line, from top left to bottom right
        for x in range(self.size - 5):
            for y in range(self.size - 5):
                score += self.getScore(color, (board[(x, y)], board[(x + 1, y + 1)],
                                               board[(x + 2, y + 2)], board[(x + 3, y + 3)], board[(x + 4, y + 4)],
                                               board[(x + 5, y + 5)]))
        # diagonal line, from top right to bottom left
        for x in range(self.size - 5):
            for y in range(self.size - 5):
                score += self.getScore(color, (board[(x + 5, y)], board[(x + 4, y + 1)],
                                               board[(x + 3, y + 2)], board[(x + 2, y + 3)], board[(x + 1, y + 4)],
                                               board[(x, y + 5)]))
        return score

    def getScore(self, color, chess):
        """
        calculate scores based on different situation
        :param color:
        :param chess:
        :return:
        """
        # highest priority, directly win
        if chess == (color, color, color, color, color, color) or chess == (
                color, color, color, color, color, 255 - color) or \
                chess == (255 - color, color, color, color, color, color) or chess == (
                -1, color, color, color, color, color) or \
                chess == (color, color, color, color, color, -1):
            return 10000

        # second priority, to prevent the opponent from winning in the next step
        if chess == (255 - color, 255 - color, 255 - color, 255 - color, color, 255 - color) or chess == (
                255 - color, color, 255 - color, 255 - color, 255 - color, 255 - color) or \
                chess == (255 - color, 255 - color, color, 255 - color, 255 - color, 255 - color) or chess == (
                255 - color, 255 - color, 255 - color, color, 255 - color, 255 - color) or \
                chess == (color, 255 - color, 255 - color, 255 - color, 255 - color, color) or \
                chess == (255 - color, 255 - color, color, 255 - color, 255 - color, -1) or chess == (
                -1, 255 - color, 255 - color, color, 255 - color, 255 - color) or \
                chess == (255 - color, color, 255 - color, 255 - color, 255 - color, -1) or chess == (
                -1, 255 - color, 255 - color, 255 - color, color, 255 - color) or \
                chess == (255 - color, color, 255 - color, 255 - color, 255 - color, color) or chess == (
                color, 255 - color, 255 - color, 255 - color, color, 255 - color) or \
                chess == (-1, 255 - color, color, 255 - color, 255 - color, 255 - color) or chess == (
                255 - color, 255 - color, 255 - color, color, 255 - color, -1):
            return 8000

        # third priority, create a must winning strategy
        if chess == (-1, color, color, color, color, -1):
            return 8000

        # fifth priority, disrupt the opponent's must winning strategy
        if chess == (-1, color, color - 255, color - 255, color - 255, -1) or chess == (
                -1, color - 255, color - 255, color - 255, color, -1) \
                or chess == (-1, color - 255, color - 255, color, color - 255, -1) or chess == (
                -1, color - 255, color, color - 255, color - 255, -1):
            return 4000
        if chess == (-1, color - 255, color - 255, -1, color - 255, color) or chess == (
                color, color - 255, -1, color - 255, color - 255, -1) or \
                chess == (-1, color - 255, -1, color - 255, color - 255, color) or chess == (
                color, color - 255, color - 255, -1, color - 255, -1):
            return 2000
        # sixth priority, create favorable chess
        if chess == (-1, color, color, color, -1, -1) or chess == (-1, -1, color, color, color, -1) or \
                chess == (-1, color, color, -1, color, -1) or chess == (-1, color, -1, color, color, -1):
            return 1000
        if chess == (-1, color, color, -1, -1, -1) or chess == (-1, -1, -1, color, color, -1) or \
                chess == (-1, -1, color, color, -1, -1) or \
                chess == (-1, color, -1, color, -1, -1) or chess == (-1, -1, color, -1, color, -1):
            return 20
        if chess == (-1, 255 - color, color, -1, -1, -1):
            if color == self.AI:
                return 10
            else:
                return 10
        return 0

    def checkWinner(self, ):
        """
        check if there is a winner come out
        :return:
        """
        winner = -1
        # horizontal
        for x in range(self.size):
            for y in range(self.size - 4):
                if self.board[(x, y)] == self.board[(x, y + 1)] == self.board[(x, y + 2)] == \
                        self.board[(x, y + 3)] == self.board[(x, y + 4)] != -1:
                    winner = self.board[(x, y)]
                    winPos = [(x, y), (x, y + 4)]
        # vertical
        for x in range(self.size - 4):
            for y in range(self.size):
                if self.board[(x, y)] == self.board[(x + 1, y)] == self.board[(x + 2, y)] == \
                        self.board[(x + 3, y)] == self.board[(x + 4, y)] != -1:
                    winner = self.board[(x, y)]
                    winPos = [(x, y), (x + 4, y)]
        # from top left to bottom right
        for x in range(self.size - 4):
            for y in range(self.size - 4):
                if self.board[(x, y)] == self.board[(x + 1, y + 1)] == self.board[(x + 2, y + 2)] == \
                        self.board[(x + 3, y + 3)] == self.board[(x + 4, y + 4)] != -1:
                    winner = self.board[(x, y)]
                    winPos = [(x, y), (x + 4, y + 4)]
        # from top right to bottom left
        for x in range(self.size - 4):
            for y in range(self.size - 4):
                if self.board[(x + 4, y)] == self.board[(x + 3, y + 1)] == self.board[(x + 2, y + 2)] == \
                        self.board[(x + 1, y + 3)] == self.board[(x, y + 4)] != -1:
                    winner = self.board[(x + 4, y)]
                    winPos = [(x + 4, y), (x, y + 4)]

        if winner != -1:
            if winner == self.AI:
                msg = "AI won!"
                print(msg)
            else:
                msg = "You won!"
                print(msg)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                        pygame.quit()
                        exit()
                self.renderBoard({"winner": msg, "winPos": winPos})
