import sys, pygame, time

pygame.init()
size = width, height = 800, 600
speed = [1,1]

black = 0,0,0

screen = pygame.display.set_mode(size)

#VARS

#boundary
bLEFT = width/10 - 30
bRIGHT = 9*width/10 + 30


#PLAYER CLASS
class Player():
    def __init__(self):
        self.x = width/10
        self.y = 9*height/10
        self.bullets = list()
        self.atkTimer = time.time()


    def checkMove(self):
        # todo: use pygame.event.get() to handle key presses
        for key in pygame.key.get_pressed():
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.x, self.y = self.move_left(self.x , self.y)
                elif keys[pygame.K_RIGHT]:
                    self.x, self.y = self.move_right(self.x, self.y) 
                    
                  

    def moveBullets(self):
        for b in self.bullets:
            b.erase()
            b.y -= 1
            b.draw()
            
    def move_left(self, x, y): 
        if(x > bLEFT):
            pygame.draw.polygon(screen, black, ((x, y), (x + 20, y + 30), (x - 20, y + 30)))
            return x - 0.005, y
        else: return x,y

    def move_right(self, x, y): 
        if(x < bRIGHT):
            pygame.draw.polygon(screen, black, ((x, y), (x + 20, y + 30), (x - 20, y + 30)))
            return x + 0.005, y
        else: return x,y
        
        
    def drawPlayer(self, x, y):
        pygame.draw.polygon(screen, (220,20,60), ((x, y), (x + 20, y + 30), (x - 20, y + 30)))
        
    def shoot(self):
        now = time.time()
        if now > self.atkTimer + 1:
            self.bullets.append(Bullet(self.x,self.y))
            self.atkTimer = time.time()
            
#TODO - bullets move at half speed when player is moving
class Bullet():
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.alive = True
        self.draw()
        
    def erase(self):
        if self.alive: pygame.draw.circle(screen, black, (self.x, self.y), 1 )
        
    def draw(self):
        if self.alive: pygame.draw.circle(screen, (255,255,255), (self.x, self.y), 1 )


#ENEMY CLASS
class Enemy():
    def __init__(self, idx, x, y):
        self.idx = idx
        self.x = x
        self.y = y
        self.alive = True
        self.instance = None
        
#ARMY CLASS
class Army():
    def __init__(self):
        self.army = list()
        self.x, self.y = int(width/10), 50
        for e in range(49): self.army.append(Enemy(e, self.x - 30, self.y ))
        self.armyTimer = time.time()
        self.lastMove = 0
        self.thisMove = "left"
        
    
    def drawArmy(self):
        screen.fill(black)
        x = self.x-30
        y = self.y
        for e in self.army:
            if e.idx == 0: pygame.draw.circle(screen, 255, (self.x - 30, self.y), 18)
            x += int(width/11)
            if e.idx in range(9,50,10): 
                y += 50
                x = int(width/11) - 22
        
                if self.lastMove <= 6: 
                    x = x + self.lastMove * 10
                elif self.lastMove > 6: 
                    x = (self.lastMove * 10) - 10
            e.x, e.y = x, y
            if e.alive: pygame.draw.circle(screen, 255, (e.x, e.y), 18)

 

    def moveArmy(self, x, y):
        now = time.time()
        if now > self.armyTimer + 1:
            
            screen.fill(black)
            #for e in self.army: 
                
            if self.lastMove < 6:
                self.x = self.x + 10
                self.drawArmy()
                self.lastMove += 1
            elif self.lastMove >= 6:
                self.x = self.x - 10
                self.drawArmy()
                self.lastMove -= 1
            if self.lastMove == 6:
                self.y = self.y + 20
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


def checkHit(bullets, army):
    for b in bullets:
        for e in army:
            #pygame.draw.polygon(screen, 255, ((e.x-20,e.y-20),(e.x-20,e.y-20),(e.x+20,e.y+20),(e.x+20,e.y-20)))
            if b.x > e.x - 20 and b.x < e.x + 20 and b.y > e.y - 20 and b.y < e.y + 20 and e.alive and b.alive:
                e.alive = False
                b.alive = False
                bullets.remove(b)
    
#GAME LOOP
while 1:
    
    #QUIT BTN
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    
    army.drawArmy()
    

    player.checkMove()
    player.drawPlayer(player.x, player.y)
    player.moveBullets()
    
    player.shoot()
    
    checkHit(player.bullets, army.army)
    
    army.moveArmy(army.x, army.y)
    pygame.display.flip()