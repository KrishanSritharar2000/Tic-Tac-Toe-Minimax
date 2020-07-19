import random
import copy

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

    def getMoveCount(self):
        return self.moveCount

    def checkWin2(self):
        # check horizontal
        for i in range(self.size):
            check = True
            for j in range(self.size - 1):
                check &= self.board[i][j] == self.board[i][j + 1]
            if check:
                return 1

        # check vertical
        for i in range(self.size):
            check = True
            for j in range(self.size - 1):
                check &= self.board[j][i] == self.board[j + 1][i]
            if check:
                return 1

        # check leading diagonal
        check = True
        for i in range(self.size - 1):
            check &= self.board[i][i] == self.board[i+1][i+1]
        if check:
            return 1
        
        #check other diagonal
        check = True
        for i in range(self.size - 1):
            check &= self.board[i][self.size - 1 - i] == self.board[i+1][self.size - i - 2]
        if check:
            return 1
        return 0

    #Return Values:
    # 0 - nothing
    # 1 - win on current board
    # 2 - can win on next move
    def checkWin(self, isMaxTurn=True):
        token = self.playerTokens[0] if isMaxTurn else self.playerTokens[1]
        currPlayerToken = self.playerTokens[1] if isMaxTurn else self.playerTokens[0]
        result = 0
        # check horizontal
        for i in range(self.size):
            checkForWin = True
            opponentTotal = 0
            for j in range(self.size):
                if (j != self.size - 1):
                    checkForWin &= self.board[i][j] == self.board[i][j + 1]
                if self.board[i][j] == token:
                    opponentTotal += 1
                else:
                    other = self.board[i][j]

            if checkForWin:
                return 1
            if (opponentTotal == self.size - 1 and other != currPlayerToken):
                result = 2

        # checkForWin vertical
        for i in range(self.size):
            checkForWin = True
            opponentTotal = 0
            for j in range(self.size):
                if (j != self.size - 1):
                    checkForWin &= self.board[j][i] == self.board[j + 1][i]
                if self.board[j][i] == token:
                    opponentTotal += 1
                else:
                    other = self.board[j][i]
            if checkForWin:
                return 1
            if (opponentTotal == self.size - 1 and other != currPlayerToken):
                result = 2

        # checkForWin leading diagonal
        checkForWin = True
        opponentTotal = 0
        for i in range(self.size):
            if (i != self.size - 1):
                checkForWin &= self.board[i][i] == self.board[i + 1][i + 1]
            if self.board[i][i] == token:
                opponentTotal += 1
            else:
                other = self.board[i][i]
        if checkForWin:
            return 1
        if (opponentTotal == self.size - 1 and other != currPlayerToken):
            result = 2
        
        #checkForWin other diagonal
        checkForWin = True
        opponentTotal = 0
        for i in range(self.size):
            if (i != self.size - 1):
                checkForWin &= self.board[i][self.size - 1 - i] == self.board[i+1][self.size - i - 2]
            if self.board[i][self.size - 1 - i] == token:
                opponentTotal += 1
            else:
                other = self.board[i][self.size - 1 - i]
        
        if checkForWin:
            return 1
        if (opponentTotal == self.size - 1 and other != currPlayerToken):
            result = 2
        return result

    @staticmethod
    #Returns the hashed value of the provided board
    def hashBoard(board):
        return "".join(["".join(row) for row in board])

    @staticmethod
    #Takes in the hash and returns a new hash with the tokens swapped 
    def hashBoardReverseToken(hashedBoard):
        return hashedBoard.replace("X", "%").replace("O", "X").replace("%", "O")

    @staticmethod
    #Takes in the hash and returns the horizontally flipped
    def hashBoardHorizontalFlip(board):
        boardToHash = board.clone().board
        boardToHashCopy = board.clone().board
        size = board.getSize()
        for i in range(size // 2):
            boardToHash[i] = boardToHashCopy[size - 1 - i]
            boardToHash[size - 1 - i] = boardToHashCopy[i]
        for i in range(size):
            for j in range(size):
                if boardToHash[i][j] not in ["X", "O"]:
                    boardToHash[i][j] = str(size * i + j)
        return board.hashBoard(boardToHash)

    @staticmethod
    #Takes in the hash and returns the vertically flipped
    def hashBoardVerticalFlip(board):
        boardToHash = board.clone().board
        boardToHashCopy = board.clone().board
        size = board.getSize() 
        for row in range(size):
            for col in range(size):
                if boardToHashCopy[row][size - 1 - col] not in ["X", "O"]:
                    boardToHash[row][col] = str(size * row + col)
                else:
                    boardToHash[row][col] = boardToHashCopy[row][size - 1 - col]
                if boardToHashCopy[row][col] not in ["X", "O"]:
                    boardToHash[row][size - 1 - col] = str(size * row + size - 1 - col)
                else:
                    boardToHash[row][size - 1 - col] = boardToHashCopy[row][col]
        return board.hashBoard(boardToHash)

   
    @staticmethod
    #Takes in the hash and returns the 90 degree clockwise flipped
    def hashBoard90Clock(board):
        boardToHash = board.clone().board
        boardToHashCopy = board.clone().board
        size = board.getSize() 
        for row in range(size):
            for col in range(size):
                if boardToHashCopy[size - 1 - col][row] not in ["X", "O"]:
                    boardToHash[row][col] = str(size * row + col)
                else:
                    boardToHash[row][col] = boardToHashCopy[size - 1 - col][row]
        return board.hashBoard(boardToHash)

    @staticmethod
    #Takes in the hash and returns the 180 degree clockwise flipped
    def hashBoard180Clock(board):
        boardToHash = board.clone().board
        boardToHashCopy = board.clone().board
        size = board.getSize() 
        for row in range(size):
            for col in range(size):
                if boardToHashCopy[size - 1 - row][size - 1 - col] not in ["X", "O"]:
                    boardToHash[row][col] = str(size * row + col)
                else:
                    boardToHash[row][col] = boardToHashCopy[size - 1 - row][size - 1 - col]
        return board.hashBoard(boardToHash)        

    @staticmethod
    #Takes in the hash and returns the 270 degree clockwise flipped
    def hashBoard270Clock(board):
        boardToHash = board.clone().board
        boardToHashCopy = board.clone().board
        size = board.getSize() 
        for row in range(size):
            for col in range(size):
                if boardToHashCopy[col][size - 1 - row] not in ["X", "O"]:
                    boardToHash[row][col] = str(size * row + col)
                else:
                    boardToHash[row][col] = boardToHashCopy[col][size - 1 - row]
        return board.hashBoard(boardToHash)        

    #Returns a clone of the current board
    def clone(self):
        b = Board(self.size, self.numOfPlayers)
        b.board = copy.deepcopy(self.board)
        b.moveCount = self.moveCount
        return b

    def clear(self):
        self.board = [[str(y * self.size + x) for x in range(self.size)]
                      for y in range(self.size)]
        self.moveCount = 0
        self.chosenColours = random.sample(self.tokenColours, self.numOfPlayers)
