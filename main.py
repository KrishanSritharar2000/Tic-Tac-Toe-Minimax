import sys
from board import *

class Game():

    def __init__(self, size=3, players=2, goFirst=True):
        assert (players > 0 and players <=6), "Only between 1 and 6 players allowed" 
        self.numOfPlayers = players
        self.playerIsFirst = goFirst
        self.board = Board(size, players)
        self.playerCounter = 0
        self.totalComp = 0
        self.playingAI = False

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
    def minimax(self, board: Board, depth: int, isMaxTurn: bool):
        self.totalComp += 1
        if board.checkWin():
            if isMaxTurn:
                return depth - 10
            return 10 - depth
        
        if board.isFull():
            return 0
        
        if isMaxTurn:
            best = -11
            for row in range(board.getSize()):
                for col in range(board.getSize()):
                    if board.isCellEmpty(row, col):
                        # TODO: refactor player token out 
                        # Make the move
                        board.move(row * board.getSize() + col, board.playerTokens[0])
                        #R Recurisively perform minimax and find the max
                        best = max(best, self.minimax(board, depth + 1, not isMaxTurn))
                        #undo the move
                        board.resetCell(row, col)
        else:
            best = 11
            for row in range(board.getSize()):
                for col in range(board.getSize()):
                    if board.isCellEmpty(row, col):
                        # TODO: refactor player token out 
                        # Make the move
                        board.move(row * board.getSize() + col, board.playerTokens[1])
                        #R Recurisively perform minimax and find the max
                        best = min(best, self.minimax(board, depth + 1, not isMaxTurn))
                        #undo the move
                        board.resetCell(row, col)
        return best

    def bestMove(self):
        bestValue = 11 if self.playerIsFirst else -11
        bestMove = -1

        for row in range(self.board.size):
            for col in range(self.board.size):
                if (self.board.isCellEmpty(row, col)):
                    self.board.move(row * self.board.getSize() + col, self.board.playerTokens[1] if self.playerIsFirst else self.board.playerTokens[0])
                    currValue = self.minimax(self.board, 0, self.playerIsFirst)# X False, O True
                    self.board.resetCell(row, col)

                    if ((self.playerIsFirst and currValue < bestValue) or 
                       (not self.playerIsFirst and currValue > bestValue)):
                        bestValue = currValue
                        bestMove = row * self.board.size + col
        print("This is the best move " + str(bestMove))
        print("Total number of comparisons " + str(self.totalComp))
        return bestMove


# sys.setrecursionlimit(10**8)        
g = Game(3, goFirst=True)
g.playAI()
# g.play()
# g.board.test()
# g.bestMove()
# g.board.printBoard()