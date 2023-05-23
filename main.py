import pygame
from pygame.locals import *
import os

YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# screen_2 = pygame.display.set_mode((SCREEN_WIDTH-100, SCREEN_HEIGHT-100))
pygame.display.set_caption('Magnetic Drawing Board')


# CURSOR IMAGE
ball_image = pygame.image.load(os.path.join('pictures','skin', 'ball.png')).convert()
ball_image.set_colorkey(BLACK)
cursor_img_width = ball_image.get_width()
cursor_img_height = ball_image.get_height()

# BACKGROUND IMAGE
SCALE = 1.8
background_image = pygame.image.load(os.path.join('pictures','screenshots', 'idea.jpg')).convert()
background_image_width = int(background_image.get_width() / SCALE)
background_image_height = int(background_image.get_height() / SCALE)
background_image_scaled = pygame.transform.scale(background_image, (background_image_width, background_image_height))

run = True
while run:

    # CURRENT CURSOR COORDINATES
    x_cord, y_cord = pygame.mouse.get_pos()

    # DRAWING
    if pygame.mouse.get_pressed()[0] == True:
        pygame.draw.circle(screen, (0,255,255,100), (x_cord, y_cord), 30)
        pygame.image.save(screen, "test.bmp")
        background_image_scaled = pygame.image.load("test.bmp").convert()
        screen.blit(background_image_scaled, (0,0))

    if pygame.mouse.get_pressed()[0] == False:
        cursor_position = pygame.mouse.get_pos()
        cursor_with_image_position = (cursor_position[0]-cursor_img_width/2, cursor_position[1]-cursor_img_height/2)
        screen.blit(background_image_scaled, (0,0))
        screen.blit(ball_image, cursor_with_image_position)

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
   
    pygame.display.update()
 
pygame.quit()