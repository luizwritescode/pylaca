import sys, pygame, time, random

pygame.display.init()
infoObject = pygame.display.Info()
size = width, height = 800, 600
speed = [1,1]

black = 0,0,0

screen = pygame.display.set_mode(size,pygame.NOFRAME+pygame.FULLSCREEN)

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
        self.pup = PowerUP(x, y)  
        self.instance = None
        
#ARMY CLASS
class Army():
    def __init__(self):
        self.army = list()
        self.x, self.y = int(width/10), 50
        x, y = self.x, self.y
        for e in range(0,49):
            x = (int(width/11) - 22) * e
            if e in range(9,50,10):
                y = 50 * e    
            self.army.append(Enemy(e, x - 30, y ))
        self.armyTimer = time.time()
        self.lastMove = 0
        self.thisMove = "left"
        
    
    def drawArmy(self):
        screen.fill(black)
        x = self.x-30
        y = self.y

        for e in self.army:
            if e.alive and e.idx == 0: pygame.draw.circle(screen, 255, (x, y), 18)
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
            

class PowerUP():
    def __init__(self, x, y):
        self.type = self.chooseType()
        self.x = x
        self.y = y

    def chooseType(self):
        n = random.randint(1,100)
        if n >= 85: return "atkSpeed"
        elif n >= 90: return "multishot"
        elif n >= 95: return "bulletSize"
        else: return "none"

    def draw(self):
        pygame.draw.circle(screen, black, (int(self.x), int(self.y)), 10)
        self.y += 0.5
        pygame.draw.circle(screen,(255,0,255),(int(self.x),int(self.y)), 10)



#INIT ENTS
player = Player()
army = Army()
pups = list()


def checkHit(bullets, army):
    for b in bullets:
        for e in army:
            #pygame.draw.polygon(screen, 255, ((e.x-20,e.y-20),(e.x-20,e.y-20),(e.x+20,e.y+20),(e.x+20,e.y-20)))
            if b.x > e.x - 20 and b.x < e.x + 20 and b.y > e.y - 20 and b.y < e.y + 20 and e.alive and b.alive:
                if e.pup.type: pups.append(e.pup)
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
    
    for p in pups:
        p.draw()
        if p.y > height: pups.remove(p)

    pygame.display.flip()