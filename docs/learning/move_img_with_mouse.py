'''
Python program to move the image with the mouse
https://www.geeksforgeeks.org/how-to-move-an-image-with-the-mouse-in-pygame/
'''

# Import the library pygame
import pygame
from pygame.locals import *
 
# Take colors input
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
 
# Construct the GUI game
pygame.init()
 
# Set dimensions of game GUI
w, h = 800, 600
screen = pygame.display.set_mode((w, h))
 
# Take image as input
img = pygame.image.load('eraser.png')
img.convert()
 
# Draw rectangle around the image
rectTT = img.get_rect()
rectTT.center = 400, 400
 

running = True
moving = False
 
while running:
     
    for event in pygame.event.get():
 
        if event.type == QUIT:
            running = False
 
        elif event.type == MOUSEBUTTONDOWN:
            if rectTT.collidepoint(event.pos):
                moving = True
 

        elif event.type == MOUSEBUTTONUP:
            moving = False
 
        elif event.type == MOUSEMOTION and moving:
            rectTT.move_ip(event.rel)
 

    screen.fill(YELLOW)
    screen.blit(img, rectTT)
    

    pygame.display.update()
 
pygame.quit()