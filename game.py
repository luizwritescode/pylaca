import sys, pygame, time

pygame.init()
size = width, height = 800, 600
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
            

    def move_left(self, x, y): 
        if(x > bLEFT):
            pygame.draw.polygon(screen, black, ((x, y), (x + 20, y + 30), (x - 20, y + 30)))
            return x - 0.1, y
        else: return x,y

    def move_right(self, x, y): 
        if(x < bRIGHT):
            pygame.draw.polygon(screen, black, ((x, y), (x + 20, y + 30), (x - 20, y + 30)))
            return x + 0.1, y
        else: return x,y
        
        
    def drawPlayer(self, x, y):
        pygame.draw.polygon(screen, (220,20,60), ((x, y), (x + 20, y + 30), (x - 20, y + 30)))



#ARMY CLASS
class Army():
    def __init__(self):
        self.army = range(50)
        self.x, self.y = int(width/10), 50
        self.armyTimer = time.time()
        self.lastMove = 0
        self.thisMove = "left"
        
    
    def drawArmy(self):
        x = self.x - 30
        y = self.y
        screen.fill(black)
        for e in self.army:
            
            if e != None: pygame.draw.circle(screen, 255, (x, y), 18)
            x += int(width/11)
            if e in range(9,50,10): 
                y += 50
                x = int(width/10) - 30
                if self.lastMove <= 6: 
                    x = x + self.lastMove * 10
                elif self.lastMove < 12: 
                    x = ((self.lastMove) * 10) - 10
                else:
                    x = x
 

    def moveArmy(self, x, y):
        now = time.time()
        if now > army.armyTimer + 1:
            
            screen.fill(black)
            
            if self.lastMove < 6:
                self.x = x + 10
                self.drawArmy()
                self.lastMove += 1
            elif self.lastMove > 6:
                self.x = x - 10
                self.drawArmy()
                self.lastMove -= 1
            else:
                self.y = y + 20
                self.drawArmy()
                if self.thisMove == "left": 
                    self.lastMove = 12
                    self.thisMove = "right"
                elif self.thisMove == "right":
                    self.lastMove = 0
                    self.thisMove = "left"   

            self.armyTimer = time.time()       

#INIT ENTS
player = Player()
army = Army()

#GAME LOOP
while 1:
    
    #QUIT BTN
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    
    army.drawArmy()
    

    player.checkMove()
    player.drawPlayer(player.x, player.y)
    

    army.moveArmy(army.x, army.y)
    pygame.display.flip()