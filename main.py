import pygame
from pygame.locals import *
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
SIZE = 100 #random.randint(50, 60)
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
cursor_selected = 'circle.bmp'

# SCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Magnetic Drawing Board')

# CURSOR IMAGE
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

# TOP BACKGROUND IMAGE
front_BG_image = pygame.image.load(Path('docs', 'skin', 'background', 'front_BG.bmp')).convert()
front_BG_image_width = int(front_BG_image.get_width() / SCALE)
front_BG_image_height = int(front_BG_image.get_height() / SCALE)
front_BG_image_scaled = pygame.transform.scale(front_BG_image, (front_BG_image_width, front_BG_image_height))
front_BG_image_scaled.set_colorkey((0, 0, 0))

run = True
while run:

    # CURRENT CURSOR COORDINATES
    x_cord, y_cord = pygame.mouse.get_pos()
    # TEMPORARY BACKGOUND PATH
    BG_temp_path = Path('docs', 'skin', 'temp', 'BG_temp.bmp')

    # DRAWING
    if pygame.mouse.get_pressed()[0] == True:
        if cursor_selected == 'circle.bmp':
            pygame.draw.circle(screen, (GREY), (x_cord, y_cord), CIRCLE_SIZE)
        elif cursor_selected == 'square.bmp':
            x_square_cord = x_cord - SQUARE_SIZE / 2
            y_square_cord = y_cord - SQUARE_SIZE / 2
            pygame.draw.rect(screen, (GREY), [x_square_cord, y_square_cord, SQUARE_SIZE, SQUARE_SIZE], 0)
        pygame.image.save(screen, BG_temp_path)
        BG_image_scaled = pygame.image.load(BG_temp_path).convert()
        screen.blit(BG_image_scaled, (0,0))

    if pygame.mouse.get_pressed()[0] == False:
        cursor_position = pygame.mouse.get_pos()
        cursor_x_coord = cursor_position[0]-cursor_img_width / 2
        cursor_y_coord = cursor_position[1]-cursor_img_height / 2
        cursor_with_image_position = (cursor_x_coord, cursor_y_coord)
        screen.blit(BG_image_scaled, (0,0))
        screen.blit(cursor_image, cursor_with_image_position)

    screen.blit(front_BG_image_scaled, (0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
   
    pygame.display.update()
 
pygame.quit()