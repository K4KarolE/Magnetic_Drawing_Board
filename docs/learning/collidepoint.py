''' COLLIDEPOINT EXAMPLE '''

from pathlib import Path
import os


WORKING_DIRECTORY = os.path.dirname(__file__)
SHAPES_DIRECTORY = Path(WORKING_DIRECTORY, 'docs', 'skin', 'shapes')

import pygame
pygame.init()
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption('GeeksForGeeks')
clock = pygame.time.Clock()


loop = True
while loop:

    # PRINT TEXT WHEN MOUSE IS OVER IMAGE
    cursor_image = pygame.image.load(Path(SHAPES_DIRECTORY, 'circle.bmp')).convert()
    cursor_image_rect = cursor_image.get_rect()
    cursor_image_rect.center = 150, 150
    screen.blit(cursor_image, cursor_image_rect)
    if cursor_image_rect.collidepoint(pygame.mouse.get_pos()):
        print('Mouse is over the image')
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
   
    pygame.display.update()
    clock.tick(60)
  
pygame.quit()