import sys, os
import pygame
import numpy as np 
import cv2
from pygame import key
from pygame import font

on = False
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("failed to open camera")
    sys.exit()

pygame.display.init()
infoObj = pygame.display.Info()

size = width, height = 800, 600
black = 0,0,0
white = 255,255,255

font.init()
font = font.SysFont("calibri", 48)
text = font.render("press space to start", False, (255,255,255))

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

screen = pygame.display.set_mode(size)
screen.blit(text, (width/2 - 200,height/2))

def start():
    
   
    
    
    return 0,0



while 1:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                break
              
    ret, frame = cap.read()
     
    screen.fill(black)
    x, y = start()
    pygame.draw.circle(screen, white, (x,y), 20)
    
    cv2.imshow("asdf", frame)
        
    #pygame.display.flip()
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    