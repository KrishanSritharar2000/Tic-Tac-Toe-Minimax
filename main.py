from board import *
from player import *

class Game():

    def __init__(self, size=3, players=2):
        self.playerTokens = ['X', 'O', '*', '$']
        self.board = Board(size)
        self.players = [Player(self.playerTokens[x]) for x in range(players)]
        self.numOfPlayers = players
        self.playerCounter = 0

    def nextPlayer(self):
        self.playerCounter += 1
        self.playerCounter %= self.numOfPlayers

    def getMove(self):
        print("Player %s's turn" % (self.playerCounter + 1))
        validMove = False
        while not validMove:
            move = input("Enter the number of the square to place your token: ")
            validMove = self.board.checkMove(move)
        self.board.move(move, self.players[self.playerCounter].getToken())
        self.board.printBoard()
        self.nextPlayer()

    def play(self):
        playAgain = True
        while playAgain:
            self.board.clear()
            self.board.printBoard() 
            self.playerCounter = 0
            while (not self.board.isFull()):
                self.getMove()
                if (self.board.checkWin()):
                    print("Player %s has won the game!" % ((self.playerCounter - 1) % self.numOfPlayers + 1))
                    break
            answer = None
            while answer not in ("yes", "no", "y", "n"):
                answer = input("Do you want to play again [Y/N]: ").lower()
            if answer in ("no", "n"):
                playAgain = False
g = Game();
g.play()