import pygame
from pygame.locals import *
import os

YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Magnetic Drawing Board')

# screen.set_colorkey(BLACK)
# pygame.draw.circle(screen, (0,0,0,50), (50, 50), 30)

#LOADING  IMAGE
ball_image = pygame.image.load(os.path.join('pictures','skin', 'ball.png'))


run = True
while run:

    # CURRENT CURSOR COORDINATES
    x_cord, y_cord = pygame.mouse.get_pos()

    # DRAWING
    if pygame.mouse.get_pressed()[0] == True:
        # x_cord, y_cord = pygame.mouse.get_pos()
        pygame.draw.circle(screen, (0,255,255,100), (x_cord, y_cord), 30)

    # ERASER
    if pygame.mouse.get_pressed()[2] == True:
        x_cord, y_cord = pygame.mouse.get_pos()
        pygame.draw.circle(screen, (255,255,100), (x_cord, y_cord), 30)
        

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
    
    # CURSOR AS AN IMAGE -> repainting the background -> drawing disappear
    screen.fill(YELLOW)
    img_width = ball_image.get_width()
    img_height = ball_image.get_height()
    cursor_position = pygame.mouse.get_pos()
    cursor_with_image_position = (cursor_position[0]-img_width/2, cursor_position[1]-img_height/2)
    screen.blit(ball_image, cursor_with_image_position)
    
    # Update the GUI pygame
    pygame.display.update()
 
# Quit the GUI game
pygame.quit()