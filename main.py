import pygame as pg #pygame, OS, random and csv modules are imported
from settings import *#Three other game files are imported
from TicTacToe import *
from os import path
class Game:#Game class is created
    def __init__(self):#game is initialised
        pg.init()#pygame module is initalised
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))#Game window is created
        pg.display.set_caption(TITLE)#Sets the title of the window
        self.clock = pg.time.Clock()#starts the internal clock to sync the game
        self.running = True
        self.font = pg.font.SysFont("helvetica",20)
        self.numOfPlayers = 2
        self.size = 3
        # self.clicked = [False for _ in range(12)]
        # self.clicked[self.numOfPlayers] = True
        # self.clicked[7 + self.size - 1] = True
        self.goToMenu()
        self.loadImages()
        self.goBack = False

    def loadImages(self):
        self.tokenImages = [None for _ in range(6)]
        self.gameFolder = path.dirname(__file__)#path to the current directory is obtained
        self.imgFolder = path.join(self.gameFolder, 'imgs')#path to the image, map and music directories are obtained

        self.tokenImages[0] =  pg.image.load(path.join(self.imgFolder, 'Xsymbol.png')).convert_alpha()
        self.tokenImages[1] =  pg.image.load(path.join(self.imgFolder, 'Osymbol.png')).convert_alpha()


    def text(self, msg, x, y, w, h, colour, size=None):
        if size != None:
            font = pg.font.SysFont("helvetica",size)
            textSurf = font.render(msg, True, colour)
        else:
            textSurf = self.font.render(msg, True, colour)
        textRect = textSurf.get_rect()
        textRect.center = (x, y)       
        self.screen.blit(textSurf, textRect)


    def button(self, msg,x,y,w,h,ic,ac,action=None, index=None, arguement=None, clickArray=None):
        if clickArray == None:
            clickArray = self.clicked
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if index == None or clickArray[index] == False:
            if (x+(w/2)) > mouse[0] > (x-(w/2)) and (y+(h/2)) > mouse[1] > (y-(h/2)):
                pg.draw.rect(self.screen, ac,((x-(w/2)), (y-(h/2)),w,h))
                if click[0] == 1:
                    if index != None:
                        clickArray[index] = True
                    down = False
                    while not down:
                        for event in pg.event.get():
                            if event.type == pg.MOUSEBUTTONUP:
                                down = True
                    if action != None:
                        if arguement != None:
                            action(arguement)         
                        else:
                            action()
            else:
                pg.draw.rect(self.screen, ic,((x-(w/2)), (y-(h/2)),w,h))
        else:
            pg.draw.rect(self.screen, ac,((x-(w/2)), (y-(h/2)),w,h))
        self.text(msg, x, y, w, h, TEXT_COLOUR)


    def run(self):#main game loop
        self.playing = True
        while self.playing:#keeps calling 'events', 'update' and 'draw' function until game is closed
            self.events()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                # pg.quit()#when while loop has stopped, call 'quit' function to unitialse and exit pygame
    
    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        screen = self.currentScreen
        screen()
        pg.display.flip()
        self.clock.tick(FPS)

    def menuScreen(self):
        self.screen.fill(BG_COLOUR)
        self.goBack = False
        self.text("Tic Tac Toe", WIDTH/2, HEIGHT/14, WIDTH, HEIGHT, TEXT_COLOUR, 24)
        self.button("Player vs AI", WIDTH/4, HEIGHT/4, WIDTH/4, HEIGHT/6, (0, 255, 0), (0, 175, 0), self.playerVsAI, 0)
        self.button("Player vs Player", 3*WIDTH/4, HEIGHT/4, WIDTH/4, HEIGHT/6, (0, 255, 0), (0, 175, 0), self.playerVsPlayer, 1)
        
        self.text("Number of Players", WIDTH/2, 7*HEIGHT/16, WIDTH, HEIGHT/12, TEXT_COLOUR)
        self.button("2", WIDTH/6, 9*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setNumOfPlayers, 2, 2)
        self.button("3", 2*WIDTH/6, 9*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setNumOfPlayers, 3, 3)
        self.button("4", 3*WIDTH/6, 9*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setNumOfPlayers, 4, 4)
        self.button("5", 4*WIDTH/6, 9*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setNumOfPlayers, 5, 5)
        self.button("6", 5*WIDTH/6, 9*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setNumOfPlayers, 6, 6)
        
        self.text("Size of Board", WIDTH/2, 11*HEIGHT/16, WIDTH, HEIGHT/12, TEXT_COLOUR)
        self.button("1", WIDTH/6, 13*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setSize, 7, 1)
        self.button("2", 2*WIDTH/6, 13*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setSize, 8, 2)
        self.button("3", 3*WIDTH/6, 13*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setSize, 9, 3)
        self.button("4", 4*WIDTH/6, 13*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setSize, 10, 4)
        self.button("5", 5*WIDTH/6, 13*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setSize, 11, 5)
        
        
        # pg.draw.rect(self.screen, (0, 255, 0), (WIDTH/2, HEIGHT/2, WIDTH/8, HEIGHT/8))

    def gameScreen(self):
        if self.play:
            self.screen.fill(BG_COLOUR)
            self.text("{} by {} Tic Tac Toe".format(self.size, self.size), WIDTH/2, HEIGHT/16, WIDTH, HEIGHT/16, TEXT_COLOUR, 24)
            self.play = False
            self.moveGiven = False       
            pg.display.flip()
            result = self.game.playGraphicalAI()
            if result == 0:
                self.text("Player has Won!", WIDTH/2, 2*HEIGHT/16, WIDTH, HEIGHT/16, TEXT_COLOUR, 24)
            elif result == 1:
                self.text("AI has Won!", WIDTH/2, 2*HEIGHT/16, WIDTH, HEIGHT/16, TEXT_COLOUR, 24)
            elif result == -1:
                self.text("The game is a Draw!", WIDTH/2, 2*HEIGHT/16, WIDTH, HEIGHT/16, TEXT_COLOUR, 24)
            self.getMove()
        self.button("Restart", 9*WIDTH/10, 2*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.playerVsAI, 12)
        self.button("Back", 1*WIDTH/10, 2*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.goToMenu, 13)
        pg.display.flip()

            

    def getMove(self):
        self.button("Restart", 9*WIDTH/10, 2*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.playerVsAI, 12)
        self.button("Back", 1*WIDTH/10, 2*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.goToMenu, 13, True)
        if self.clicked[13]:
            self.goBack = True
            self.clicked[13] = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        length = self.size + 2
        for row in range(self.game.board.size):
            for col in range(self.game.board.size):
                if self.game.board.isCellEmpty(row, col):
                    self.button("", (row + 1) * WIDTH/length + WIDTH/(length*2) ,(col + 1) * HEIGHT/length + HEIGHT/(length*2), WIDTH/length, HEIGHT/length, BG_COLOUR, (120, 120, 120), index=row*self.game.board.size+col, clickArray=self.buttonClick)
                    
                    if self.buttonClick[row * self.game.board.size + col]:
                        self.moveGiven = True
                        self.moveGivenBoard = row * self.game.board.size + col
                else:
                    image = pg.transform.scale(self.tokenImages[self.game.board.playerTokens.index(self.game.board.board[row][col])], (int(WIDTH/length), int(HEIGHT/length)))
                    
                    rect = image.get_rect()
                    rect.topleft = ((row + 1) * WIDTH/length ,(col + 1) * HEIGHT/length)
                    
                    self.screen.blit(image, rect)
                
        for i in range(self.size - 1):
            pg.draw.line(self.screen, BLACK, ((2+i)*WIDTH/length, HEIGHT/length), ((2+i)*WIDTH/length, (length-1)*HEIGHT/length))
                # pg.draw.line(self.screen, BLACK, (2*WIDTH/5, HEIGHT/5), (2*WIDTH/5, 4*HEIGHT/5))
                # pg.draw.line(self.screen, BLACK, (3*WIDTH/5, HEIGHT/5), (3*WIDTH/5, 4*HEIGHT/5))
            pg.draw.line(self.screen, BLACK, (WIDTH/length, (2+i)*HEIGHT/length), ((length-1)*WIDTH/length, (2+i)*HEIGHT/length))
                # pg.draw.line(self.screen, BLACK, (WIDTH/5, 2*HEIGHT/5), (4*WIDTH/5, 2*HEIGHT/5))
                # pg.draw.line(self.screen, BLACK, (WIDTH/5, 3*HEIGHT/5), (4*WIDTH/5, 3*HEIGHT/5))
     


        # if self.size == 1:
        #     pass
        # elif self.size == 2:
        #     pass
        # elif self.size == 3:
        #     for row in range(self.game.board.size):
        #         for col in range(self.game.board.size):
        #             if self.game.board.isCellEmpty(row, col):
        #                 self.button("", (row + 1) * WIDTH/5 + WIDTH/10 ,(col + 1) * HEIGHT/5 + HEIGHT/10, WIDTH/5, HEIGHT/5, BG_COLOUR, (120, 120, 120), index=row*self.game.board.size+col, clickArray=self.buttonClick)
        #                 if self.buttonClick[row * self.game.board.size + col]:
        #                     self.moveGiven = True
        #                     self.moveGivenBoard = row * self.game.board.size + col
        #             else:
        #                 image = pg.transform.scale(self.tokenImages[self.game.board.playerTokens.index(self.game.board.board[row][col])], (int(WIDTH/5), int(HEIGHT/5)))
        #                 rect = image.get_rect()
        #                 rect.topleft = ((row + 1) * WIDTH/5 ,(col + 1) * HEIGHT/5)
        #                 self.screen.blit(image, rect)
                    
        #     pg.draw.line(self.screen, BLACK, (2*WIDTH/5, HEIGHT/5), (2*WIDTH/5, 4*HEIGHT/5))
        #     pg.draw.line(self.screen, BLACK, (3*WIDTH/5, HEIGHT/5), (3*WIDTH/5, 4*HEIGHT/5))
        #     pg.draw.line(self.screen, BLACK, (WIDTH/5, 2*HEIGHT/5), (4*WIDTH/5, 2*HEIGHT/5))
        #     pg.draw.line(self.screen, BLACK, (WIDTH/5, 3*HEIGHT/5), (4*WIDTH/5, 3*HEIGHT/5))


        # elif self.size == 4:
        #     pass
        # elif self.size == 5:
        #     pass
        pg.display.flip()

    def goToMenu(self, back=False):
        self.currentScreen = self.menuScreen
        self.clicked = [False for _ in range(14)]
        self.clicked[self.numOfPlayers] = True
        self.clicked[7 + self.size - 1] = True
        if back:
            self.clicked[13] = True


    def setNumOfPlayers(self, players):
        self.clicked[self.numOfPlayers] = False
        self.numOfPlayers =  players

    def setSize(self, size):
        self.clicked[7 + self.size - 1] = False
        self.size = size

    def playerVsAI(self):
        self.currentScreen = self.gameScreen
        self.play = True
        self.clicked[12] = False
        self.buttonClick = [False for _ in range(self.size * self.size)]
        self.game = TicTacToe(self.size, 2, True, 10, False, True, self)

    def playerVsPlayer(self):
        self.currentScreen = self.gameScreen
        self.play = True
        self.clicked[12] = False
        self.buttonClick = [False for _ in range(self.size * self.size)]
        self.game = TicTacToe(self.size, self.numOfPlayers, True, 10, False, False, self)

g = Game()#create and instance of the 'Game' class

# while g.running:#whilst 'running' variable is TRUE
#     g.new()#call the 'new' function
g.run()
pg.quit()