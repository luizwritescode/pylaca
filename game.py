import sys, pygame

pygame.init()
size = width, height = 1080, 820
speed = [1,1]

black = 0,0,0

screen = pygame.display.set_mode(size)

#VARS

#boundary
bLEFT = width/10
bRIGHT = 9*width/10


#PLAYER CLASS
class Player():
    def __init__(self):
        self.x = width/10
        self.y = 9*height/10


    def checkMove(self):

        
        # todo: use pygame.event.get() to handle key presses
        for key in pygame.key.get_pressed():
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.x, self.y = self.move_left(self.x , self.y)
                elif keys[pygame.K_RIGHT]:
                    self.x, self.y = self.move_right(self.x, self.y) 
            

    def move_left(self ,x, y): 
        if(x > bLEFT):
            screen.fill(black)
            return x - 0.1, y
        else: return x,y

    def move_right(self, x,y): 
        if(x < bRIGHT):
            screen.fill(black)
            return x + 0.1, y
        else: return x,y


#FUCTIONS

def drawArmy(army):
    x, y = int(width/10), 100
    for e in army:
        if e != None: pygame.draw.circle(screen, 255, (x,y), 18)
        x += int(width/11)
        if e in range(9,50,10): 
            y += 50
            x = int(width/10)
        pygame.display.flip()

def drawPlayer(x, y):
    pygame.draw.polygon(screen, 123, ((x, y), (x + 20, y + 30), (x - 20, y + 30)))

#INIT ENTS
player = Player()
army = range(50)

#GAME LOOP
while 1:
    
    #QUIT BTN
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    drawArmy(army)

    player.checkMove()
    drawPlayer(player.x, player.y)
    

    pygame.display.flip()