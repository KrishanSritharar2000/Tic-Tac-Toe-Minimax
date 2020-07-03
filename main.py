import sys
from board import *
import time

class Game():

    def __init__(self, size=3, players=2, goFirst=True, maxDepth=1000000):
        assert (players > 0 and players <=6), "Only between 1 and 6 players allowed" 
        self.numOfPlayers = players
        self.playerIsFirst = goFirst
        self.maxDepth = maxDepth
        self.board = Board(size, players)
        self.playerCounter = 0
        self.totalComp = 0
        self.playingAI = False
        self.maxScore = self.board.getSize() * self.board.getSize() + 1

    def __nextPlayer(self):
        self.playerCounter += 1
        self.playerCounter %= self.numOfPlayers

    def __getMove(self):
        if self.playingAI:
            print("\033[0mPlayer's turn")
        else:
            print("\033[0mPlayer %s's turn" % (self.playerCounter + 1))
        validMove = False
        while not validMove:
            move = input("Enter the number of the square to place your token: ")
            validMove = self.board.checkMove(move)
        self.board.move(int(move), self.board.getPlayerToken(self.playerCounter))
        self.board.printBoard()
        self.__nextPlayer()

    def __getAIMove(self):
        self.board.move(self.bestMove(), self.board.getPlayerToken(self.playerCounter))
        self.board.printBoard()
        self.__nextPlayer()

    def playAI(self):
        self.playingAI = True
        playAgain = True
        while playAgain:
            self.board.clear()
            self.board.printBoard()
            #below for AI vs AI
            #self.playerCounter = 1 if self.playerIsFirst else 0
            self.playerCounter = 0
            draw = True
            if self.playerIsFirst:
                self.__getMove()
            self.__getAIMove()
            while (not self.board.isFull()):
                #Get move from player
                self.__getMove()
                if (self.board.checkWin()):
                    print("\033[0mCongratulations, You have won the game!" )
                    draw = False
                    break
                #Make AI move
                if not self.board.isFull():
                    self.__getAIMove()
                    #below for AI vs AI
                    # self.playerIsFirst = not self.playerIsFirst
                    if (self.board.checkWin()):
                        print("\033[0mThe AI has won the game!" )
                        draw = False
                        break
                    self.totalComp = 0

            if (draw):
                print("\033[0mThe game has ended in a draw!")

            answer = None
            while answer not in ("yes", "no", "y", "n"):
                answer = input("Do you want to play again [Y/N]: ").lower()
            if answer in ("no", "n"):
                playAgain = False
    
    def play(self):
        self.playingAI = False
        playAgain = True
        while playAgain:
            self.board.clear()
            self.board.printBoard()
            self.playerCounter = 0
            draw = True
            while (not self.board.isFull()):
                self.__getMove()
                if (self.board.checkWin()):
                    print("\033[0mPlayer %s has won the game!" % ((self.playerCounter - 1) % self.numOfPlayers + 1))
                    draw = False
                    break

            if (draw):
                print("\033[0mThe game has ended in a draw!")
            answer = None
            while answer not in ("yes", "no", "y", "n"):
                answer = input("Do you want to play again [Y/N]: ").lower()
            if answer in ("no", "n"):
                playAgain = False

    # Maximiser is always the player
    def minimax(self, board: Board, depth: int, maxDepth: int, isMaxTurn: bool, alpha: int, beta: int):
        self.totalComp += 1
        if board.checkWin():
            if isMaxTurn:
                return depth - self.maxScore
            return self.maxScore - depth
        
        if board.isFull() or depth == maxDepth:
            return 0
        
        if isMaxTurn:
            best = -1000000
            for row in range(board.getSize()):
                for col in range(board.getSize()):
                    if board.isCellEmpty(row, col):
                        # TODO: refactor player token out 
                        # Make the move
                        board.move(row * board.getSize() + col, board.playerTokens[0])
                        # Recurisively perform minimax and find the max
                        currValue = self.minimax(board, depth + 1, maxDepth, False, alpha, beta)
                        best = max(best, currValue)
                        #undo the move
                        board.resetCell(row, col)
                        #pruning
                        alpha = max(alpha, currValue)
                        if beta <= alpha:
                            break
                else:
                    continue
                break
        else:
            best = 1000000
            for row in range(board.getSize()):
                for col in range(board.getSize()):
                    if board.isCellEmpty(row, col):
                        # TODO: refactor player token out 
                        # Make the move
                        board.move(row * board.getSize() + col, board.playerTokens[1])
                        # Recurisively perform minimax and find the max
                        currValue = self.minimax(board, depth + 1, maxDepth, True, alpha, beta)
                        best = min(best, currValue)
                        #undo the move
                        board.resetCell(row, col)
                        #pruning
                        beta = min(beta, currValue)
                        if beta <= alpha:
                            break
                else:
                    continue
                break
        return best

    def bestMove(self):
        bestValue = 1000000 if self.playerIsFirst else -1000000
        bestMove = -1
        bestMoves = [i for i in range(self.board.getSize() * self.board.getSize())]
        print(bestMoves)
        counter = 0
        start = time.time()
        for row in range(self.board.size):
            for col in range(self.board.size):
                if (self.board.isCellEmpty(row, col)):
                    self.board.move(row * self.board.getSize() + col, self.board.playerTokens[1] if self.playerIsFirst else self.board.playerTokens[0])
                    currValue = self.minimax(self.board, 0, self.maxDepth, self.playerIsFirst, -1000000, 1000000)# X False, O True
                    self.board.resetCell(row, col)
                    print("This is currValue: {} for row: {} col: {} move: {}".format(currValue, row, col, row * self.board.size + col))

                    if (currValue == bestValue):
                        bestMoves[counter] = row * self.board.size + col
                        counter += 1

                    if ((self.playerIsFirst and currValue < bestValue) or 
                       (not self.playerIsFirst and currValue > bestValue)):
                        bestValue = currValue
                        bestMove = row * self.board.size + col
                        counter = 0
                        bestMoves[counter] = bestMove
                        counter += 1
                    

                    #If there is a win on the next move, stop and dont try any more
                    if ((self.playerIsFirst and bestValue == -self.maxScore) or
                        (not self.playerIsFirst and bestValue == self.maxScore)):
                        break
            else:
                continue
            break

        print("This is the best move " + str(bestMove))
        print("Total number of comparisons " + str(self.totalComp))
        print("Total time taken: " + str(time.time() - start))
        if (counter > 0):
            return random.choice(bestMoves[:counter])
        return bestMove


# sys.setrecursionlimit(10**8)        
g = Game(size=4, maxDepth=8, goFirst=True)
g.playAI()
# g.play()
# g.board.test()
# g.bestMove()
# g.board.printBoard()