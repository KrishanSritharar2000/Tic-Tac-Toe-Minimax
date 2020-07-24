import pygame as pg #pygame, OS, random and csv modules are imported
from settings import *#Three other game files are imported
from TicTacToe import *
class Game:#Game class is created
    def __init__(self):#game is initialised
        pg.init()#pygame module is initalised
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))#Game window is created
        pg.display.set_caption(TITLE)#Sets the title of the window
        self.clock = pg.time.Clock()#starts the internal clock to sync the game
        self.running = True
        self.clicked = [0 for _ in range(12)]
        self.font = pg.font.SysFont("helvetica",20)
        self.numOfPlayers = 2
        self.size = 3
        self.clicked[self.numOfPlayers] = True

    def text(self, msg, x, y, w, h, colour):
        textSurf = self.font.render(msg, True, colour)
        textRect = textSurf.get_rect()
        textRect.center = (x, y)       
        self.screen.blit(textSurf, textRect)


    def button(self, msg,x,y,w,h,ic,ac,action=None, index=None, arguement=None):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if index == None or self.clicked[index] == False:
            if (x+(w/2)) > mouse[0] > (x-(w/2)) and (y+(h/2)) > mouse[1] > (y-(h/2)):
                pg.draw.rect(self.screen, ac,((x-(w/2)), (y-(h/2)),w,h))

                if click[0] == 1 and action != None:
                    if index != None:
                        self.clicked[index] = True
                    down = False
                    while not down:
                        for event in pg.event.get():
                            if event.type == pg.MOUSEBUTTONUP:
                                down = True
                    if arguement != None:
                        action(arguement)         
                    else:
                        action()
            else:
                pg.draw.rect(self.screen, ic,((x-(w/2)), (y-(h/2)),w,h))
        else:
            pg.draw.rect(self.screen, ac,((x-(w/2)), (y-(h/2)),w,h))
        self.text(msg, x, y, w, h, (0, 0, 0))


    def run(self):#main game loop
        self.playing = True
        self.currentScreen = self.menuScreen
        while self.playing:#keeps calling 'events', 'update' and 'draw' function until game is closed
        #     self.dt = self.clock.tick(FPS) / 1000 #get the time of the previous frame in seconds
            self.events()
            # self.update()
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
        print("players", self.numOfPlayers, "size", self.size)
        self.screen.fill((255,255,255))
        self.button("Player vs AI", WIDTH/4, HEIGHT/4, WIDTH/4, HEIGHT/6, (0, 255, 0), (0, 175, 0), self.playerVsAI, 0)
        self.button("Player vs Player", 3*WIDTH/4, HEIGHT/4, WIDTH/4, HEIGHT/6, (0, 255, 0), (0, 175, 0), self.playerVsPlayer, 1)
        
        self.text("Number of Players", WIDTH/2, 7*HEIGHT/16, WIDTH, HEIGHT/12, (0,0,0))
        self.button("2", WIDTH/6, 9*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setNumOfPlayers, 2, 2)
        self.button("3", 2*WIDTH/6, 9*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setNumOfPlayers, 3, 3)
        self.button("4", 3*WIDTH/6, 9*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setNumOfPlayers, 4, 4)
        self.button("5", 4*WIDTH/6, 9*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setNumOfPlayers, 5, 5)
        self.button("6", 5*WIDTH/6, 9*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setNumOfPlayers, 6, 6)
        
        self.text("Size of Board", WIDTH/2, 11*HEIGHT/16, WIDTH, HEIGHT/12, (0,0,0))
        self.button("1", WIDTH/6, 13*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setSize, 7, 1)
        self.button("2", 2*WIDTH/6, 13*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setSize, 8, 2)
        self.button("3", 3*WIDTH/6, 13*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setSize, 9, 3)
        self.button("4", 4*WIDTH/6, 13*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setSize, 10, 4)
        self.button("5", 5*WIDTH/6, 13*HEIGHT/16, WIDTH/8, HEIGHT/8, (0, 255, 0), (0, 175, 0), self.setSize, 11, 5)
        
        
        # pg.draw.rect(self.screen, (0, 255, 0), (WIDTH/2, HEIGHT/2, WIDTH/8, HEIGHT/8))

    def gameScreen(self):
        print("game screen")

    def setNumOfPlayers(self, players):
        self.clicked[self.numOfPlayers] = False
        self.numOfPlayers =  players

    def setSize(self, size):
        self.clicked[7+self.size - 1] = False
        self.size = size

    def playerVsAI(self):
        print("Clicked")
        self.currentScreen = self.gameScreen 
        self.game = TicTacToe(self.size, 2, True, 10, False, True)

    def playerVsPlayer(self):
        print("Clicked")
        self.currentScreen = self.gameScreen 
        self.game = TicTacToe(self.size, self.numOfPlayers, True, 10, False, False)

g = Game()#create and instance of the 'Game' class

# while g.running:#whilst 'running' variable is TRUE
#     g.new()#call the 'new' function
g.run()
x = input('')