import sys, pygame, time, random, os
import numpy as np
from video import Tracking

pygame.init()
pygame.font.init()
pygame.display.init()
infoObject = pygame.display.Info()

speed = [1,1]

black = 0,0,0
white = 255,255,255
gray = 127,127,127
green = 0,255,0
red = 255,0,0
yellow = 255,255,0


font = pygame.font.SysFont("namco.ttf", 32)
#VARS

#RESOLUTION
resolution = [(1920,1080), (1366,768), (1280,720), (800, 600)]
size = width, height = 800, 600
fullscreen = 0

if(len(sys.argv) > 2): 
    size = width, height = resolution[int(sys.argv[1])]
    if(int(sys.argv[2]) == 0): fullscreen = pygame.NOFRAME+pygame.FULLSCREEN


    

#boundary
bLEFT = width/10 - 30
bRIGHT = 9*width/10 + 30


#LOAD IMAGES
logo = pygame.image.load('assets\\pylagalogo.png')
logo = pygame.transform.scale(logo, (logo.get_width()//4, logo.get_height()//4))

starship = pygame.image.load('assets\\starship.gif')
starship = pygame.transform.scale(starship, (starship.get_width()//4, starship.get_height()//4))


#PLAYER CLASS
class Player():
    def __init__(self):
        self.surf = pygame.surface.Surface(starship.get_size(), pygame.SRCALPHA, 32)
        self.x = width//2
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
        keys = pygame.key.get_pressed()
        self.moveBullets()
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
        #pygame.draw.polygon(screen, (220,20,60), ((x, y), (x + 20, y + 30), (x - 20, y + 30)))
        screen.blit(starship, (x - 23,y))
        
        
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
        for e in range(50):
            x += (int(width/11) - 30) * e
            if e in range(0,50,10):
                y = 50 * e
                x = width // 11    
            self.army.append(Enemy(e, x, y))
        self.armyTimer = time.time()
        self.lastMove = 0
        self.thisMove = "left"
        self.speed = 1
        
    
    def drawArmy(self):
        x = self.x
        y = self.y
        for e in self.army:
            e.x, e.y = x, y
            if e.alive: pygame.draw.circle(screen, 255, (e.x, e.y), 18)
            x += int(width/11)
            if e.idx in range(9,50,10): 
                y += 50
                x = int(width/11) - 22
        
                if self.lastMove <= 6: 
                    x = x + self.lastMove * 10
                elif self.lastMove > 6: 
                    x = (self.lastMove * 10) - 10
            

 
    def moveArmy(self, x, y):
        now = time.time()
        if now > self.armyTimer + self.speed:
            
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
    
    def setSpeed(self, speed):
        self.speed = speed
            

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

def drawBackground(surf):
    T.run()
    tScreen = T.get_screen()
    if (tScreen is not None):
        tScreen = 255*tScreen//tScreen
        surf = pygame.surfarray.make_surface(tScreen)
        surf = pygame.transform.flip(surf, False, True)
        surf = pygame.transform.rotate(surf, -90)
        surf = pygame.transform.scale(surf, size)

    surf.set_alpha(50)
    screen.blit(surf, (0,0))

class Menu():
    def __init__(self):
        self.surf = pygame.surface.Surface(size, pygame.SRCALPHA)
        self.action = None
        self.blink = False
        self.blinkTimer = time.time()
        self.blinkDelay = 1000
        self.play_btn_color = white
        self.quit_btn_color = white

    def drawMenu(self):
        if(self.action == "PLAY"):
            self.play_btn_color = self.blink()
        elif(self.action == "QUIT"):
            self.quit_btn_color = self.blink()
    
        
        self.play_btn = pygame.draw.rect(self.surf, self.play_btn_color, (width//12, height//3, width//4, height//3), 1)
        self.play_text = font.render("jogar", 1, (self.play_btn_color))
        self.surf.blit(self.play_text, (self.play_btn.centerx - self.play_text.get_width()//2 , self.play_btn.centery - self.play_text.get_height()//2 ))

        self.quit_btn = pygame.draw.rect(self.surf, self.quit_btn_color, (8*width//12, height//3, width//4, height//3), 1)
        self.quit_text = font.render("sair", 1, (self.quit_btn_color))
        self.surf.blit(self.quit_text, (self.quit_btn.centerx - self.quit_text.get_width()//2 , self.quit_btn.centery - self.quit_text.get_height()//2 ))

        screen.blit(logo, (width//2 - logo.get_width()//2, height//10))

        screen.blit(self.surf, (0,0))

    def drawDifficulty(self):
        self.easy = pygame.draw.rect(self.surf, green, (width//12, height//3, width//4, height//3), 1)
        self.easy_text = font.render("facil", 1, (self.play_btn_color))
        self.surf.blit(self.easy_text, (self.easy.centerx - self.easy_text.get_width()//2 , self.easy.centery - self.easy_text.get_height()//2 ))

        self.hard = pygame.draw.rect(self.surf, red, (8*width//12, height//3, width//4, height//3), 1)
        self.hard_text = font.render("dificil", 1, (self.quit_btn_color))
        self.surf.blit(self.hard_text, (self.hard.centerx - self.hard_text.get_width()//2 , self.hard.centery - self.hard_text.get_height()//2 ))

        screen.blit(logo, (width//2 - logo.get_width()//2, height//10))

        screen.blit(self.surf, (0,0))


    def checkHit(self, bullets):
        hit = False
        for b in bullets:
            if b.x < self.play_btn.right and b.x > self.play_btn.left and b.y < self.play_btn.bottom:
                self.action = "PLAY"
                hit = True
    
            elif  b.x < self.quit_btn.right and b.x > self.quit_btn.left and b.y < self.quit_btn.bottom:
                self.action = "QUIT"
        if hit:
            self.clearSurface()
            player.bullets = list()
            player.x = width//2

    def checkHitDifficulty(self, bullets):
        hit = False
        for b in bullets:
            if b.x < self.easy.right and b.x > self.easy.left and b.y < self.easy.bottom:
                self.action = "EASY"
                hit = True
            elif  b.x < self.hard.right and b.x > self.hard.left and b.y < self.hard.bottom:
                self.action = "HARD"
                hit = True

        if hit:
            self.clearSurface()
            player.bullets = list()
            player.x = width//2
         
    def blink(self):
        now = time.time()
        if now > self.blinkTimer + self.blinkDelay:
            self.blink = True
            self.blinkTimer = time.time()
            return yellow
        else:
            self.blink = False
            return white

    def clearSurface(self):
        self.surf = pygame.surface.Surface(size, pygame.SRCALPHA)

def drawAim(move_x):
    surf = pygame.surface.Surface(size, pygame.SRCALPHA)

    if(move_x < width//2 - width//12 or move_x > width//2 + width//12):
        move_x = False
    elif(move_x): 
        aim_rim = pygame.draw.circle(surf, white, (move_x, move_y), 5, 1)
    
    color = gray
    if move_x:
        color = white

    surf.set_alpha(200)
    
    pygame.draw.rect(surf, color, (width//2 - width//12, height//2, 2, 120))
    pygame.draw.rect(surf, color, (width//2 + width//12, height//2, 2, 120))
            
    screen.blit(surf, (0,0))

def fadeOut(a, surf):
    surf.set_alpha(a)
    return a - 1

if __name__ == "__main__":
    screen = pygame.display.set_mode(size,fullscreen)
    T = Tracking()  

    SHOW_MENU = True
    running = True   
    while running:
        MENU_SCREEN = "root"

        #INIT ENTS
        player = Player()
        army = Army()
        pups = list()
        end = False
        started = False

        bg_surface = pygame.surface.Surface(size)

        if(SHOW_MENU):
            menu = Menu()
            while menu:
                screen.fill(black)
                drawBackground(bg_surface)

                if MENU_SCREEN == "root":
                    menu.drawMenu()
                    menu.checkHit(player.bullets)
                elif MENU_SCREEN == "diff":
                    menu.drawDifficulty()
                    menu.checkHitDifficulty(player.bullets)


                move_x, move_y = player.checkMove(T.get_movement(), True)

                drawAim(move_x)
                player.drawPlayer(player.x, player.y)


                if menu.action == "PLAY":
                    MENU_SCREEN = "diff"
                elif menu.action == "EASY":
                    army.setSpeed(1)
                    SHOW_MENU = False
                    break
                elif menu.action == "HARD":
                    army.setSpeed(0.5)
                    SHOW_MENU = False
                    break
                elif menu.action == "QUIT":
                    sys.exit()

                    
                if(move_x):
                    player.shoot()

                for event in pygame.event.get():
                    keys = pygame.key.get_pressed()
                    if event.type == pygame.QUIT: sys.exit()
                    elif keys[pygame.K_q] : sys.exit()
                    elif keys[pygame.K_ESCAPE] : sys.exit()
                    if event.type == pygame.KEYDOWN:
                        pass
                pygame.display.update()
        else:
            player.x = bLEFT
            move = None
            count = 0

            #GAME LOOP
            while 1:

                #draw bg
                screen.fill(black)

                army.drawArmy()

                #run tracking and grab screen
                drawBackground(bg_surface)
                
                #QUIT BTN
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: sys.exit()
                    elif pygame.key.get_pressed()[pygame.K_q] : sys.exit()
                    elif pygame.key.get_pressed()[pygame.K_ESCAPE] : sys.exit()
                
                
                #draw aim position
                aim_alpha = 50
                aim_surface = pygame.surface.Surface(size, pygame.SRCALPHA, 32)

                # START CONDITION
                
                move_x, move_y = player.checkMove(T.get_movement(), started)

                if(move_x):
                    last_move = move_x
                if(last_move > (width//2)-15 and last_move < (width//2) + 15):
                    count += 1
                else:
                    count = 0
                
                if( count > 50):
                    started = True

                #draw aim instructions
                if(not started and not end):
                    instructions = font.render("segure a mira no meio do circulo para jogar", 1, (white))
                    textpos = instructions.get_rect()
                    screen.blit(instructions, ((width // 2)-textpos.centerx, 11 * height // 12))
                    pygame.draw.circle(aim_surface, white, (width//2, height//2 + 60), 10, 1)
                    #progress bar
                    if count > 0:
                        pygame.draw.rect(aim_surface, (64,64,64), (width//2 - width//12, height//2 + height//5, width//6, 2))
                        pygame.draw.rect(aim_surface, white, (width//2 - width//12, height//2 + height//5, (count/50)*width//6, 2))


                if(move_x < width//2 - width//12 or move_x > width//2 + width//12):
                    move_x = False
                elif(move_x): 
                    aim_alpha = 128
                    pygame.draw.circle(aim_surface, white, (move_x, move_y), 5)
                
                aim_surface.set_alpha(aim_alpha)
                pygame.draw.rect(aim_surface, white, (width//2 - width//12, height//2, 2, 120))
                pygame.draw.rect(aim_surface, white, (width//2 + width//12, height//2, 2, 120))
                
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
                end = True
                deaths = 0
                for e in army.army:
                    if e.alive:
                        end = False
                    else:
                        deaths = deaths + 1
                    if e.y > 9*height//10 and e.alive:
                        end = True
                        break
                
                win = False
                if deaths == 50:
                    win = True
                
                        
                #GAMEOVER SCREEN
                if end: 
                    started = False
                    text = font.render("GAME OVER", 1, (white))
                    textpos = text.get_rect()
                    textpos.centerx = screen.get_rect().centerx
                    textpos.centery = screen.get_rect().centery
                    screen.blit(text, (textpos.centerx - text.get_width() // 2, textpos.centery - text.get_height() // 2))
                    endTimer = 0
                    while endTimer < 1000:
                        endTimer = endTimer + 1
                        pygame.display.update()
                    end = False
                    SHOW_MENU = True
                    break
                
                win = True
                if win:
                    started = False
                    text = font.render("YOU WIN", 1, (white))
                    textpos = text.get_rect()
                    textpos.centerx = screen.get_rect().centerx
                    textpos.centery = screen.get_rect().centery
                    screen.blit(text, (textpos.centerx - text.get_width() // 2, textpos.centery - text.get_height() // 2))
                    endTimer = 0
                    while endTimer < 5000:
                        endTimer = endTimer + 1
                        pygame.display.update()
                    win = False
                    SHOW_MENU = True
                    break

                pygame.display.update()
