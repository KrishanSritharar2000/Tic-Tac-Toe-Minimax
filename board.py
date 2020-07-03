import random

class Board():
    def __init__(self, size=3, players=2):
        self.size = size
        self.playerTokens = ['X', 'O', '*', '$', '&', '?']
        self.numOfPlayers = players
        self.tokenColours = ["\033[1;31;40m", "\033[1;34;40m", "\033[1;35;40m", "\033[1;36;40m", "\033[1;33;40m", "\033[1;95;40m"]
        self.clear()
        self.moveCount = 0
        self.boardColour = "\033[1;32;40m"

    def getPlayerToken(self, playerCounter):
        assert (playerCounter >= 0 and playerCounter < self.numOfPlayers)
        return self.playerTokens[playerCounter]

    def printBoard(self):
        border = ['_' for i in range(self.size*5*2 + 1)]
        border = ''.join(border)
        print(self.boardColour + border)
        for row in self.board:
            print('|', end='')
            for i in range(self.size):
                print("         |", end='')
            print('\n|', end='')

            for col in row:
                space = "    "#4 space characters
                if col in self.playerTokens:
                    printedCol = self.chosenColours[self.playerTokens.index(col)] + col + self.boardColour
                else:
                    printedCol = "\033[1;30m" + col + self.boardColour
                    if (int(col) >= 1000):
                        space = " "
                    elif (int(col) >= 100):
                        space = "  "
                    elif (int(col) >= 10):
                        space = "   " 
                print(space + printedCol + "    |", end='')
            print("\n|", end='')

            for i in range(self.size):
                print("_________|", end='')
            print("\n", end='')

    # move is the number representing the position on the board
    def checkMove(self, move):
        if (int(move) < 0 or int(move) > self.size * self.size):
            # Not a valid number on grid
            return False
        # if point on board == move then in empty
        return self.board[int(move) // self.size][int(move) % self.size] == move

    # PRE: checkMove was tested     
    def move(self, move, token):
        if self.checkMove(str(move)):
            self.board[move // self.size][move % self.size] = token
            self.moveCount += 1

    def isFull(self):
        return self.moveCount >= self.size * self.size

    def isCellEmpty(self, row, col):
        assert 0 <= row and row < self.size, "Invalid Row" 
        assert 0 <= col and col < self.size, "Invalid Column" 
        return self.board[row][col] == str(row * self.size + col)

    def resetCell(self, row, col):
        assert 0 <= row and row < self.size, "Invalid Row" 
        assert 0 <= col and col < self.size, "Invalid Column" 
        self.board[row][col] = str(row * self.size + col)
        self.moveCount -= 1

    def getSize(self):
        return self.size

    def checkWin(self):
        # check horizontal
        for i in range(self.size):
            check = True
            for j in range(self.size - 1):
                check &= self.board[i][j] == self.board[i][j + 1]
            if check:
                return True

        # check vertical
        for i in range(self.size):
            check = True
            for j in range(self.size - 1):
                check &= self.board[j][i] == self.board[j + 1][i]
            if check:
                return True

        # check leading diagonal
        check = True
        for i in range(self.size - 1):
            check &= self.board[i][i] == self.board[i+1][i+1]
        if check:
            return True
        
        #check other diagonal
        check = True
        for i in range(self.size - 1):
            check &= self.board[i][self.size - 1 - i] == self.board[i+1][self.size - i - 2]
        return check

    def clear(self):
        self.board = [[str(y * self.size + x) for x in range(self.size)]
                      for y in range(self.size)]
        self.moveCount = 0
        self.chosenColours = random.sample(self.tokenColours, self.numOfPlayers)

    def test(self):
        self.board = [['X', '1', '2', '3'],
                      ['4', 'O', '6', '7'],
                      ['8', 'O', '10', '11'],
                      ['12', 'O', '14', '15']]
                      
        self.moveCount = 4
        #1146973
        #11048697