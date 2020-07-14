import sys, time, ctypes, pickle
from board import *
from multiprocessing import Process, Value, Array


class Game():

    def __init__(self, size=3, players=2, goFirst=True, maxDepth=1000000, concurrent=True):
        assert (players > 0 and players <=6), "Only between 1 and 6 players allowed" 
        self.numOfPlayers = players
        self.playerIsFirst = goFirst
        self.maxDepth = maxDepth
        self.board = Board(size, players)
        self.playerCounter = 0
        self.totalComp = 0
        self.concurrent = concurrent
        self.playingAI = False
        self.maxScore = self.board.getSize() * self.board.getSize() + 1
        self.tableName = str(size) + "size" + str(size) + "inRow"
        self.loadMoveTable()

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
        if self.concurrent:
            self.board.move(self.bestMoveConcurrent(), self.board.getPlayerToken(self.playerCounter))
        else:
            self.board.move(self.bestMove(), self.board.getPlayerToken(self.playerCounter))
        self.board.printBoard()
        self.__nextPlayer()

    def loadMoveTable(self):
        try:
            tableFile = open(self.tableName, "rb")
            self.moveTable = pickle.load(tableFile)
            tableFile.close()
            print("table loaded, loaded files {}".format(len(self.moveTable)))
        except FileNotFoundError as e:
            self.moveTable = {}
            print("table created")
    
    def saveMoveTable(self):
        tableFile = open(self.tableName, "wb")
        pickle.dump(self.moveTable, tableFile)
        print("saved file size {}".format(len(self.moveTable)))
        tableFile.close()

    def train(self, loops):
        start = time.time()
        self.playingAI = True
        playAgain = 0
        first = 0
        second = 0
        try:
            while playAgain < loops:
                self.board.clear()
                self.board.printBoard()
                #below for AI vs AI
                # self.playerCounter = 1 if self.playerIsFirst else 0
                self.playerCounter = 0
                draw = True
                self.playerIsFirst = False
                self.__getAIMove()
                while (not self.board.isFull()):
                    #Get first move from AI
                    self.playerIsFirst = True
                    self.__getAIMove()
                    if (self.board.checkWin() == 1):
                        print("\033[0mThe AI going second has won the game!")
                        second += 1
                        draw = False
                        break
                    #Make second AI move
                    if not self.board.isFull():
                        self.playerIsFirst = False
                        self.__getAIMove()
                        #below for AI vs AI
                        # self.playerIsFirst = not self.playerIsFirst
                        if (self.board.checkWin() == 1):
                            print("\033[0mThe AI going first has won the game!")
                            first += 1
                            draw = False
                            break
                        self.totalComp = 0

                if (draw):
                    print("\033[0mThe game has ended in a draw!")
                playAgain += 1
                print("New game")
        finally:
            self.saveMoveTable() 
            print("Time Taken {}".format(time.time()- start))  
            print("First Won {} Second Won {}".format(first, second))   

    def playAI(self):
        self.playingAI = True
        playAgain = True
        try:
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
                    if (self.board.checkWin() == 1):
                        print("\033[0mCongratulations, You have won the game!" )
                        draw = False
                        break
                    #Make AI move
                    if not self.board.isFull():
                        self.__getAIMove()
                        #below for AI vs AI
                        # self.playerIsFirst = not self.playerIsFirst
                        if (self.board.checkWin() == 1):
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
        finally:
            self.saveMoveTable()
    
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
                if (self.board.checkWin() == 1):
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

    def inMoveTable(self, board, reverse=False):
        if reverse:
            hashedTable = Board.hashBoard(board.board)
            reversedTable = Board.hashBoardReverseToken(hashedTable)
            if reversedTable in self.moveTable:
                return self.moveTable[reversedTable]
            
            hashedTable = Board.hashBoardHorizontalFlip(board)
            reversedTable = Board.hashBoardReverseToken(hashedTable)
            if reversedTable in self.moveTable:
                return self.moveTable[reversedTable]
            
            hashedTable = Board.hashBoardVerticalFlip(board)
            reversedTable = Board.hashBoardReverseToken(hashedTable)
            if reversedTable in self.moveTable:
                return self.moveTable[reversedTable]

            hashedTable = Board.hashBoard90Clock(board)
            reversedTable = Board.hashBoardReverseToken(hashedTable)
            if reversedTable in self.moveTable:
                return self.moveTable[reversedTable]

            hashedTable = Board.hashBoard180Clock(board)
            reversedTable = Board.hashBoardReverseToken(hashedTable)
            if reversedTable in self.moveTable:
                return self.moveTable[reversedTable]
            
            hashedTable = Board.hashBoard270Clock(board)
            reversedTable = Board.hashBoardReverseToken(hashedTable)
            if reversedTable in self.moveTable:
                return self.moveTable[reversedTable]
        else:
            #Normal Hash
            hashedTable = Board.hashBoard(board.board)
            if hashedTable in self.moveTable:
                return self.moveTable[hashedTable]
        
            #Horizontal Flip
            hashedTable = Board.hashBoardHorizontalFlip(board)
            if hashedTable in self.moveTable:
                return self.moveTable[hashedTable]
            
            #Vertical Flip
            hashedTable = Board.hashBoardVerticalFlip(board)
            if hashedTable in self.moveTable:
                return self.moveTable[hashedTable]
            
            #90 Degree Rotation
            hashedTable = Board.hashBoard90Clock(board)
            if hashedTable in self.moveTable:
                return self.moveTable[hashedTable]
            
            #180 Degree Rotation
            hashedTable = Board.hashBoard180Clock(board)
            if hashedTable in self.moveTable:
                return self.moveTable[hashedTable]
            
            #270 Degree Rotation
            hashedTable = Board.hashBoard270Clock(board)
            if hashedTable in self.moveTable:
                return self.moveTable[hashedTable]
        
        return None
    # Maximiser is always the player
    #288103
    #376968
    def minimax(self, board: Board, depth: int, maxDepth: int, isMaxTurn: bool, alpha: int, beta: int):
        self.totalComp += 1

        if isMaxTurn:
            hashedResult = self.inMoveTable(board, True)
        else:
            hashedResult = self.inMoveTable(board, False)
    
        if hashedResult is not None:
            return hashedResult

            # if isMaxTurn:
            #     return hashedResult
            # return hashedResult

        result = board.checkWin(isMaxTurn)
        if result == 1:
            if isMaxTurn:
                return depth - self.maxScore
            return self.maxScore - depth
        
        #heuristic checking if opponent can win on next move
        if result == 2:
            if isMaxTurn:
                return self.maxScore - depth - 1
            return depth - self.maxScore + 1


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
        if isMaxTurn:
            self.moveTable[Board.hashBoardReverseToken(Board.hashBoard(board.board))] = best
        else:
            self.moveTable[Board.hashBoard(board.board)] = best
        return best


    def bestMove(self):
        bestValue = 1000000 if self.playerIsFirst else -1000000
        bestMove = -1
        bestMoves = [i for i in range(self.board.getSize() * self.board.getSize())]
        counter = 0
        start = time.time()
        if self.board.getMoveCount() == 0:
            print("Total number of comparisons " + str(self.totalComp))
            print("Total time taken: " + str(time.time() - start))
            return random.choice(bestMoves)

        for row in range(self.board.size):
            for col in range(self.board.size):
                if (self.board.isCellEmpty(row, col)):
                    self.board.move(row * self.board.getSize() + col, self.board.playerTokens[1] if self.playerIsFirst else self.board.playerTokens[0])
                    # # check if in move table
                    if self.playerIsFirst:
                        hashedResult = self.inMoveTable(self.board, True)
                    else:
                        hashedResult = self.inMoveTable(self.board, False)
                    if hashedResult is not None:
                        currValue = hashedResult
                        #     # if self.playerIsFirst: # "O" turn
                        # #     #     currValue = hashedResult
                        # #     # else:
                        # #     #     currValue = -hashedResult
                    else:
                        currValue = self.minimax(self.board, 0, self.maxDepth, self.playerIsFirst, -1000000, 1000000)# X False, O True  
                        if self.playerIsFirst:
                            self.moveTable[Board.hashBoardReverseToken(Board.hashBoard(self.board.board))] = currValue
                        else:
                            self.moveTable[Board.hashBoard(self.board.board)] = currValue
                            
                        # if self.playerIsFirst:
                        #     self.moveTable[self.board.hashBoard(self.board.board)] = currValue
                        # else:
                        #     self.moveTable[self.board.hashBoard(self.board.board)] = -currValue
                    
                    # currValue = self.minimax(self.board, 0, self.maxDepth, self.playerIsFirst, -1000000, 1000000)# X False, O True  

                    self.board.resetCell(row, col)
                    print("This is currValue: {} for row: {} col: {} move: {} max: {} hash : {}".format(currValue, row, col, row * self.board.size + col, self.playerIsFirst, 0))

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

        print("This is the best move " + str(bestMoves[:counter]))
        print("Total number of comparisons " + str(self.totalComp))
        print("Total time taken: " + str(time.time() - start))
               
        if (counter > 0):
            return random.choice(bestMoves[:counter])
        return bestMove

    # Maximiser is always the player
    # @jit(target = "cuda")
    # @jit
    def minimaxConcurrent(self, board: Board, depth: int, maxDepth: int, isMaxTurn: bool, alpha: int, beta: int, totalComparisons: Value):
        totalComparisons.value += 1

        hashedResult = self.inMoveTable(board)
        if hashedResult is not None:
            return hashedResult

        result = board.checkWin(isMaxTurn)
        if result == 1:
            if isMaxTurn:
                return depth - self.maxScore
            return self.maxScore - depth

        if result == 2:
            if isMaxTurn:
                return self.maxScore
            return -self.maxScore

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
                        currValue = self.minimaxConcurrent(board, depth + 1, maxDepth, False, alpha, beta, totalComparisons)
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
                        currValue = self.minimaxConcurrent(board, depth + 1, maxDepth, True, alpha, beta, totalComparisons)
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
        self.moveTable[Board.hashBoard(board.board)] = best
        return best

    def callMinimaxConcurrent(self, row, col, board, depth, maxDepth, isMaxTurn, alpha, beta, counter, bestMovesArray, bestValueSingle, totalComparisons, stop):
        board.move(row * board.getSize() + col, self.board.playerTokens[1] if isMaxTurn else self.board.playerTokens[0])

        #check if in move table
        hashedResult = self.inMoveTable(board)
        if hashedResult is not None:
            currValue = hashedResult
        else:
            currValue = self.minimaxConcurrent(board, depth, maxDepth, isMaxTurn, alpha, beta, totalComparisons)# X False, O True
            self.moveTable[Board.hashBoard(board.board)] = currValue
        print("This is currValue: {} for row: {} col: {} move: {} Maximiser: {}".format(currValue, row, col, row * board.getSize() + col, isMaxTurn))

        board.resetCell(row, col)
        with bestValueSingle.get_lock():
            if (currValue == bestValueSingle.value):
                with counter.get_lock():
                    with bestMovesArray.get_lock():
                        bestMovesArray[counter.value] = row * board.getSize() + col
                        counter.value += 1

            if ((isMaxTurn and currValue < bestValueSingle.value) or 
                (not isMaxTurn and currValue > bestValueSingle.value)):
                bestValueSingle.value = currValue
                with counter.get_lock():
                    # counter.value = 0
                    with bestMovesArray.get_lock():
                        bestMovesArray[0] = row * board.getSize() + col
                    counter.value = 1
            #If there is a win on the next move, stop and dont try any more
            if ((isMaxTurn and bestValueSingle.value == -self.maxScore) or
                (not isMaxTurn and bestValueSingle.value == self.maxScore)):
                stop[0] = True

    def bestMoveConcurrent(self):
        start = time.time()
        if self.board.getMoveCount() == 0:
            print("Total number of comparisons 0") 
            print("Total time taken: " + str(time.time() - start))
            return random.choice([i for i in range(self.board.getSize() * self.board.getSize())])

        bestValueSingle = Value(ctypes.c_long, 1000000 if self.playerIsFirst else -1000000)
        counter = Value(ctypes.c_int, 0)
        bestMovesArray = Array(ctypes.c_int, range(self.board.getSize() * self.board.getSize()))
        threads = []
        totalComp = Value(ctypes.c_int, 0)
        stop = [False]

        row = 0
        while (not stop[0] and row < self.board.size):
            col = 0
            while (not stop[0] and col < self.board.size):
                if (self.board.isCellEmpty(row, col)):
                    threads.append(Process(target=self.callMinimaxConcurrent, args=(row, col, self.board.clone(), 0, self.maxDepth, self.playerIsFirst, -1000000, 1000000, counter, bestMovesArray, bestValueSingle, totalComp, stop)))
                col += 1
            row += 1         

        print("Total number of threads " + str(len(threads)))
        for thread in threads:            
            thread.start()

        for thread in threads:
            if stop[0]:
                for thread in threads:
                    thread.terminate()
            else:
                thread.join()


        with counter.get_lock():
            with bestMovesArray.get_lock():
                print("This is the best move " + str(bestMovesArray[0]))
                print("Total number of comparisons " + str(totalComp.value))
                print("Total time taken: " + str(time.time() - start))
                if (counter.value > 0):
                    return random.choice(bestMovesArray[:counter.value])
                return bestMovesArray[0]

if __name__ == '__main__':
    # sys.setrecursionlimit(10**8)        
    g = Game(size=3, goFirst=False, maxDepth=10, concurrent=False)
    # g.playAI()
    g.train(100)
    #91
    
    #307
    #3254

    #346
    #140418
    #195 743
    #373000
    #434087
    #435424
    # g.maxScore = 4 * 4 + 1
    board = Board(3)
    board.board = [['0', 'X', 'O'],
                    ['3', 'O', '5'],
                    ['6', 'X', '8']]
    #print("Hash", g.moveTable[Board.hashBoard(board.board)])
    print("Hashed", Board.hashBoard(board.board))
    board.moveCount = 4
    # board = Board(4)
    # board.board = [['O', 'O', 'X', 'X'],
    #                 ['X', 'X', '6', '7'],
    #                 ['O', 'O', 'O', '11'],
    #                 ['12', 'X', '14', '15']]
    # board.moveCount = 10
    # board2 = Board(4)
    # board2.board = [['0', 'O', 'X', 'O'],
    #               ['X', 'O', 'X', 'O'],
    #               ['8', 'O', '10', 'X'],
    #               ['12', '13', '14', 'X']]
    # board2.moveCount = 10
    # board3 = Board(4)
    # board3.board = [['1', '1', '2', 'O'],
    #               ['X', 'X', 'O', '7'],
    #               ['8', 'X', 'O', '11'],
    #               ['12', '13', '14', '15']]
    # board3.moveCount = 4
    # # self.moveCount = 4
    # hashedBoard = Board.hashBoard(board.board)
    # reverseHashedBoard = Board.hashBoardReverseToken(hashedBoard)
    # print(hashedBoard)
    # print(reverseHashedBoard)
    # currValue1 = g.minimax(board, 0, 10, True, -1000000, 1000000)# X False, O True  
    # currValue2 = g.minimax(board2, 0, 10, True, -1000000, 1000000)# X False, O True  
    # currValue3 = g.minimax(board3, 0, 10, True, -1000000, 1000000)# X False, O True  
    
    # print("Value 1 ", currValue1)
    # g.saveMoveTable()
    # print("Value 2 ", currValue2)
    # print("Value 3 ", currValue3)

    g.board = board
    g.playerIsFirst = True
    bestMove1 = g.bestMove()
    # g.saveMoveTable()
    # g.board = board2
    # g.playerIsFirst = True
    # bestMove2 = g.bestMove()
    # g.board = board3
    # g.playerIsFirst = False
    # bestMove3 = g.bestMove()
    # g.board.printBoard()
    
    print("Best move 1", bestMove1)
    # board.printBoard()
    # print("Best move 2", bestMove2)
    # print("Best move 3", bestMove3)

    # board.printBoard()
    # board2.printBoard()

    # print(Board.hashBoardReverseToken(Board.hashBoard(board.board)))

    # print(Board.hashBoardReverseToken(Board.hashBoardVerticalFlip(board)))
    # board2 = Board(4)
    # board2.board = [['X', '1', '2', '3'],
    #                 ['4', 'O', '6', '7'],
    #                 ['8', 'O', '10', '11'],
    #                 ['12', 'O', '14', '15']]


    #187243
    # g.train(50)
    #record 3x3
    #92
    #101
    #257
    #467
    #563


    #record of move table for 4x4
    #0
    #After train(1) 210581

    # g.play()
    # g.board.test()
    # g.bestMove()
    # g.board.printBoard()

    #389551
    #1 688 696
    #1 701 186