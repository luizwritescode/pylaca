import sys, os
import pygame
from pygame import key
from pygame import font
from pygaze import eyetracker
from pygaze import libinput


pygame.display.init()
infoObj = pygame.display.Info()

size = width, height = 1366, 768
print(size)

black = 0,0,0

font.init()
font = font.SysFont("calibri", 48)
text = font.render("press space to start", False, (255,255,255))

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

pygame.display.init()

screen = pygame.display.set_mode(size)

screen.blit(text, (width/2 - 200,height/2))
tracker = eyetracker.EyeTracker(screen)


def start():
    tracker.calibrate()
    tracker.start_recording()
    
    t1, startpos = tracker.wait_for_saccade_start()
    endtime, startpos, endpos = tracker.wait_for_saccade_end()
    
    tracker.stop_recording() 
    
    return endpos

on = False

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                on = True    
    
    if on: 
        screen.fill(black)
        x, y = start()
        print(x, y)
        pygame.draw.circle(screen, 255, (x,y), 20)
        
    pygame.display.flip()
    
    
    