import sys, pygame, time, random
import numpy as np
from video import Tracking

pygame.init()
pygame.font.init()
pygame.display.init()
infoObject = pygame.display.Info()
size = width, height = 800, 600
speed = [1,1]

black = 0,0,0
white = 255,255,255

screen = pygame.display.set_mode(size)#,pygame.NOFRAME)#+pygame.FULLSCREEN)
font = pygame.font.SysFont("consolas.ttf", 72)
#VARS

#boundary
bLEFT = width/10 - 30
bRIGHT = 9*width/10 + 30

T = Tracking()

#PLAYER CLASS
class Player():
    def __init__(self):
        self.x = width/10
        self.y = 9*height/10
        self.bullets = list()
        self.atkTimer = time.time()
        self.atkSpeed = 1
        self.moveSpeed = 1
        self.bulletSize = 3

    def moveBullets(self):
        for b in self.bullets:
            b.erase()
            b.y -= 5
            b.draw()

    def checkMove(self, face_movement = False, started = False):
        # todo: use pygame.event.get() to handle key presses
        keys = pygame.key.get_pressed()
        self.moveBullets()
        print(face_movement)
        x = y = False
        if(face_movement):
            self.moveSpeed = abs(face_movement/10)
            x = width//2 + face_movement
            y = height//2 + 60
        
        if(started and face_movement):
            if face_movement < 0:
                self.x, self.y = self.move_left(self.x , self.y)
            elif face_movement > 0:
                self.x, self.y = self.move_right(self.x, self.y) 

        return x, y    
                    
                  
    def powerup(self, pup):
        if pup.type == 0:
            self.atkSpeed = 0.5
    
            
    def move_left(self, x, y): 
        if(x > bLEFT):
            pygame.draw.polygon(screen, black, ((x, y), (x + 20, y + 30), (x - 20, y + 30)))
            return x - self.moveSpeed, y
        else: return x,y

    def move_right(self, x, y): 
        if(x < bRIGHT):
            pygame.draw.polygon(screen, black, ((x, y), (x + 20, y + 30), (x - 20, y + 30)))
            return x + self.moveSpeed, y
        else: return x,y
        
        
    def drawPlayer(self, x, y):
        pygame.draw.polygon(screen, (220,20,60), ((x, y), (x + 20, y + 30), (x - 20, y + 30)))
        
    def shoot(self):
        now = time.time()
        if now > self.atkTimer + self.atkSpeed:
            b = Bullet(self.x, self.y)
            b.size = self.bulletSize
            self.bullets.append(b)
            self.atkTimer = time.time()
            
#TODO - bullets move at half speed when player is moving
class Bullet():
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.alive = True
        self.size = 1
        self.draw()
        
    def erase(self):
        if self.alive: pygame.draw.circle(screen, black, (self.x, self.y), self.size )
        
    def draw(self):
        if self.alive: pygame.draw.circle(screen, (255,255,255), (self.x, self.y), self.size )


#ENEMY CLASS
class Enemy():
    def __init__(self, idx, x, y):
        self.idx = idx
        self.x = x
        self.y = y
        self.alive = True 
        self.pup = PowerUP(x, y)  
        self.instance = None
    
    def die(self):
        pygame.draw.circle(screen, black, (self.x, self.y), 18)
        
#ARMY CLASS
class Army():
    def __init__(self):
        self.army = list()
        self.x, self.y = int(width/10) - 30, 50
        x, y = self.x, self.y
        for e in range(49):
            x += (int(width/11) - 30) * e
            if e in range(0,50,10):
                y = 50 * e
                x = width // 11    
            self.army.append(Enemy(e, x, y))
        self.armyTimer = time.time()
        self.lastMove = 0
        self.thisMove = "left"
        
    
    def drawArmy(self):
        screen.fill(black)
        x = self.x
        y = self.y
        for e in self.army:
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
        self.alive = True

    def chooseType(self):
        n = random.randint(1,100)
        if n >= 85: 
            self.color = (255,0,255)
            return {0:"atkSpeed"}
        elif n >= 90: 
            self.color = (0,255,255)
            return {1:"multishot"}
        elif n >= 95: 
            self.color = (255,255,0)
            return {2:"bulletSize"}
        else: return None

    def draw(self, b = True):
        pygame.draw.circle(screen, black, (int(self.x), int(self.y)), 10)
        self.y += 0.2
        if b:
            pygame.draw.circle(screen,self.color,(int(self.x),int(self.y)), 10)



#INIT ENTS
player = Player()
army = Army()
pups = list()
end = True
started = False

def checkHit(bullets, army):
    for b in bullets:
        for e in army:
            #pygame.draw.polygon(screen, 255, ((e.x-20,e.y-20),(e.x-20,e.y-20),(e.x+20,e.y+20),(e.x+20,e.y-20)))
            if b.x > e.x - 20 and b.x < e.x + 20 and b.y > e.y - 20 and b.y < e.y + 20 and e.alive and b.alive:
                if e.pup.type: 
                    e.pup.x = e.x
                    e.pup.y = e.y
                    pups.append(e.pup)
                e.die()
                e.alive = False
                b.alive = False
                bullets.remove(b)

def gameover():
    
    i = 0
    while i < 10000000000:
        i += 1
    sys.exit()

def put_array(surface, myarr):          # put array into surface
    bv = surface.get_view("0")
    bv.write(myarr.tostring())

if __name__ == "__main__":
    MENU = False

    if(MENU):
        drawMenu()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pass
    else:
        bg_surface = pygame.surface.Surface(size)
        move = None
        count = 0
        #GAME LOOP
        while 1:
            army.drawArmy()

            #draw bg
            
            T.run()
            tScreen = T.get_screen()
            if(tScreen is not None):
                tScreen = 255*tScreen/tScreen
                bg_surface = pygame.surfarray.make_surface(tScreen)
                bg_surface = pygame.transform.flip(bg_surface, False, True)
                bg_surface = pygame.transform.rotate(bg_surface, -90)
                bg_surface = pygame.transform.scale(bg_surface, size)

            bg_surface.set_alpha(50)
            screen.blit(bg_surface, (0,0))
            
            #QUIT BTN
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                elif pygame.key.get_pressed()[pygame.K_q] : sys.exit()
            
            
            #draw aim position

            aim_alpha = 50
            aim_surface = pygame.surface.Surface(size, pygame.SRCALPHA, 32)

            if(not started):
                pygame.draw.circle(aim_surface, white, (width//2, height//2 + 60), 10, 1)

            move_x, move_y = player.checkMove(T.get_movement(), started)

            # START CONDITION
            if((move_x > -10 or move_x < 10) and move_x != 0):
                count += 1
            
            if( count > 50):
                started = True

            if(move_x < width//2 - width//12 or move_x > width//2 + width//12):
                move_x = False
            elif(move_x): 
                aim_alpha = 255
                pygame.draw.circle(aim_surface, white, (move_x, move_y), 5)
            
            aim_surface.set_alpha(aim_alpha)
            pygame.draw.rect(aim_surface, white, (width//2 - width//12, height//2, 5, 120))
            pygame.draw.rect(aim_surface, white, (width//2 + width//12, height//2, 5, 120))
            
            screen.blit(aim_surface, (0,0))
            player.drawPlayer(player.x, player.y)


            

            if(started):
                player.shoot() 
                checkHit(player.bullets, army.army)
            
                army.moveArmy(army.x, army.y)
            
            #POWERUPS - not implemented
            for p in pups:
                if p.y > height - 10:
                    pups.remove(p)
                elif p.x > player.x and p.x < player.x + 20 and p.y > player.y and p.y < player.y + 30:
                    player.powerup(p)
                    pups.remove(p)
                else: pass#p.draw()
            
            #GAMEOVER CHECK
            for e in army.army:
                if e.alive:
                    end = False
            #GAMEOVER SCREEN
            if end: 
                screen.fill(black)
                text = font.render("GAME OVER", 1, (white))
                textpos = text.get_rect()
                textpos.centerx = screen.get_rect().centerx
                textpos.centery = screen.get_rect().centery
                screen.blit(text, (textpos.centerx - text.get_width() // 2, textpos.centery - text.get_height() // 2))

            pygame.display.flip()
