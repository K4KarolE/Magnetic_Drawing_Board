''' 
PyGame Set Mouse Cursor from Bitmap
https://www.geeksforgeeks.org/pygame-set-mouse-cursor-from-bitmap/
'''

import pygame
import os
from pathlib import Path

pygame.init()

WORKING_DIRECTORY = os.path.dirname(__file__)
SHAPES_DIRECTORY = Path(WORKING_DIRECTORY, 'docs', 'skin', 'shapes')


# Creating a canvas of 600*400
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

# sandard cursor
# pygame.mouse.set_cursor()
  
# old type, "bitmap" cursor
cursor1 = pygame.cursors.diamond
  
# new type, "system" cursor
cursor2 = pygame.SYSTEM_CURSOR_HAND

cursor_image = pygame.image.load(Path(SHAPES_DIRECTORY, 'circle.bmp')).convert()
cursor_image.set_colorkey('Black')


''' WITH IMAGE'''
surf = pygame.Surface((80, 80), pygame.SRCALPHA)
surf.blit(cursor_image, (0,0))
cursor3 = pygame.cursors.Cursor((40, 40), surf)

''' WITH DRAWING'''
# surf = pygame.Surface((30, 25), pygame.SRCALPHA)
# pygame.draw.rect(surf, (0, 255, 0), [0, 0, 10, 10])
# pygame.draw.rect(surf, (0, 255, 0), [20, 0, 10, 10])
# pygame.draw.rect(surf, (255, 0, 0), [5, 5, 20, 20])
# cursor3 = pygame.cursors.Cursor((15, 5), surf)
  
cursors = [cursor1, cursor2, cursor3]
cursor_index = 0
  
# the arguments to set_cursor can be a Cursor object
# or it will construct a Cursor object
# internally from the arguments
pygame.mouse.set_cursor(cursors[cursor_index])
  
while True:
    screen.fill("white")
  
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            cursor_index += 1
            cursor_index %= len(cursors)
            pygame.mouse.set_cursor(cursors[cursor_index])
  
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
  
    pygame.display.flip()
    clock.tick(144)