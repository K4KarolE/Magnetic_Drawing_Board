import pygame
# from pygame.locals import *
from pathlib import Path
import os
import random

# COLORS
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREY = (192, 192, 192)

#SCREEN
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#SHAPES
SHAPES_DIRECTORY = Path('docs', 'skin', 'shapes')
SIZE = 40 #random.randint(50, 60)
shape_size_dict = {
    'circle.bmp': SIZE,
    'square.bmp': SIZE * 1.8,
    'star.bmp': SIZE
    }

CIRCLE_SIZE = shape_size_dict['circle.bmp']
SQUARE_SIZE = shape_size_dict['square.bmp']

pygame.init()

# GENERATING SHAPES
def generating_shapes():

    shape_list = os.listdir(SHAPES_DIRECTORY)

    for item in shape_list:
        if pygame.image.load(Path(SHAPES_DIRECTORY, item)).get_width() != shape_size_dict[item]:
            # CIRCLE
            if item == 'circle.bmp':
                SIDE = shape_size_dict['circle.bmp'] * 2
                screen_shape = pygame.display.set_mode((SIDE, SIDE))
                screen_shape.fill(BLACK)
                pygame.draw.circle(screen_shape, (GREY), (SIDE/2, SIDE/2), CIRCLE_SIZE)
                pygame.image.save(screen_shape, Path(SHAPES_DIRECTORY, 'circle.bmp'))
            # SQUARE
            if item == 'square.bmp':
                screen_shape = pygame.display.set_mode((SQUARE_SIZE, SQUARE_SIZE))
                screen_shape.fill(BLACK)
                pygame.draw.rect(screen_shape, (GREY), [0, 0, SQUARE_SIZE, SQUARE_SIZE], 0)
                pygame.image.save(screen_shape, Path(SHAPES_DIRECTORY, 'square.bmp'))

generating_shapes()

cursor_selected = 'square.bmp'
cursor_selected = None
cursor_selected = 'circle.bmp'

# SCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Magnetic Drawing Board')

# CURSOR IMAGE
if cursor_selected:
    cursor_image = pygame.image.load(Path('docs','skin','shapes', cursor_selected)).convert()
    cursor_image.set_colorkey(BLACK)
    cursor_img_width = cursor_image.get_width()
    cursor_img_height = cursor_image.get_height()

# BACKGROUND IMAGE
SCALE = 1.8
BG_image = pygame.image.load(Path('docs', 'skin', 'background', 'BG.jpg')).convert()
BG_image_width = int(BG_image.get_width() / SCALE)
BG_image_height = int(BG_image.get_height() / SCALE)
BG_image_scaled = pygame.transform.scale(BG_image, (BG_image_width, BG_image_height))

# FRONT BACKGROUND IMAGE - WITH NO DRAWING SURFACE
front_BG_image = pygame.image.load(Path('docs', 'skin', 'background', 'front_BG.bmp')).convert()
front_BG_image_width = int(front_BG_image.get_width() / SCALE)
front_BG_image_height = int(front_BG_image.get_height() / SCALE)
front_BG_image_scaled = pygame.transform.scale(front_BG_image, (front_BG_image_width, front_BG_image_height))
front_BG_image_scaled.set_colorkey((0, 0, 0))

run = True
# DRAWING_SURFACE_X = [105, 187]
# DRAWING_SURFACE_Y = [100, 160]
while run:

    # CURRENT CURSOR COORDINATES
    x_coord, y_coord = pygame.mouse.get_pos()
    # CURSOR IMAGE COORDINATES 
    if cursor_selected:
        cursor_with_image_position = (x_coord - cursor_img_width/2, y_coord - cursor_img_height/2)
    # TEMPORARY BACKGROUND
    BG_temp_path = Path('docs', 'skin', 'temp', 'BG_temp.bmp')

    # DRAWING & SAVING THE MODIFIED BG IMAGE
    if pygame.mouse.get_pressed()[0] == True:
        if cursor_selected:
            if cursor_selected == 'circle.bmp':
                pygame.draw.circle(screen, (GREY), (x_coord, y_coord), CIRCLE_SIZE)
            elif cursor_selected == 'square.bmp':
                pygame.draw.rect(screen, (GREY), [cursor_with_image_position[0], cursor_with_image_position[1], SQUARE_SIZE, SQUARE_SIZE], 0)
        pygame.image.save(screen, BG_temp_path)
        BG_image_scaled = pygame.image.load(BG_temp_path).convert()
        screen.blit(BG_image_scaled, (0,0))

    # DISPLAY THE CURSOR IMAGE(if selected) 
    # & DISPLAY THE BG (the previously modified if drawing already actioned)
    if pygame.mouse.get_pressed()[0] == False:
        screen.blit(BG_image_scaled, (0,0))
        if cursor_selected:
            screen.blit(cursor_image, cursor_with_image_position)
    # DISPLAY THE FRONT/FRAME IMAGE - WITH NO DRAWING SURFACE
    screen.blit(front_BG_image_scaled, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
   
    pygame.display.update()
 
pygame.quit()