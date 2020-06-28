class Board():
    def __init__(self, size=3):
        self.board = [[str(y * size + x) for x in range(size)] for y in range(size)]
        self.size = size

    def printBoard(self):
        border = ['_' for i in range(self.size*5*2 + 1)]
        border = ''.join(border)
        print(border)
        for row in self.board:
            print("|         |         |         |")
            print('|', end='')
            for col in row:
                print("    " + col + "    |", end='')
            print("\n|_________|_________|_________|")
