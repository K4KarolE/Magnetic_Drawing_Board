import pygame
from pathlib import Path
import os

# COLORS
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREY = (192, 192, 192)


#SCREEN
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# PATHS
WORKING_DIRECTORY = os.path.dirname(__file__)
SHAPES_DIRECTORY = Path(WORKING_DIRECTORY, 'docs', 'skin', 'shapes')
BACKGROUND_DIRECTORY = Path(WORKING_DIRECTORY, 'docs', 'skin', 'background')
BG_TEMP_PATH = Path(WORKING_DIRECTORY, 'docs', 'skin', 'temp', 'BG_temp.bmp')

# SHAPES AND SIZES
SIZE = 30
shape_size_dict = {
    'circle.bmp': SIZE,
    'square.bmp': SIZE * 1.8,
    'star.bmp': SIZE
    }

CIRCLE_SIZE = shape_size_dict['circle.bmp']
SQUARE_SIZE = shape_size_dict['square.bmp']

shape_selected = None

## CURSOR / SURFACE MAP
# DRAWING SURFACE
DRAWING_SURFACE = {
    'x': range(210, 670),
    'y': range(105, 430)
    }
# CIRCLE - SHAPE SELECTION
CIRCLE_SHAPE_SELECT = {
    'x': range(110, 170),
    'y': range(110, 170)
    }
# SQUARE - SHAPE SELECTION
SQUARE_SHAPE_SELECT = {
    'x': range(80, 130),
    'y': range(190, 250)
    }

# SHAPE SELECTED/DESELECTED COUNTER
counter_circle, counter_square = [1, 1]

pygame.init()

clock = pygame.time.Clock()

# GENERATING SHAPES - IF SIZE CHANGES
def generating_shapes():

    shape_list = os.listdir(SHAPES_DIRECTORY)

    for item in shape_list:
        if pygame.image.load(Path(SHAPES_DIRECTORY, item)).get_width() != shape_size_dict[item]:
            # CIRCLE
            if item == 'circle.bmp':
                SIDE = shape_size_dict['circle.bmp'] * 2    # just for the 'screen_shape' screen -> to generate new image
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

# SCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Magnetic Drawing Board')

# BACKGROUND IMAGE
SCALE = 1.8
BG_image = pygame.image.load(Path(BACKGROUND_DIRECTORY, 'BG.jpg')).convert()
BG_image_width = int(BG_image.get_width() / SCALE)
BG_image_height = int(BG_image.get_height() / SCALE)
BG_image_scaled = pygame.transform.scale(BG_image, (BG_image_width, BG_image_height))

run = True
while run:

    # SHAPE SELECTED/DESELECTED COUNTER
    circle_selected = counter_circle % 2 == 0
    square_selected = counter_square % 2 == 0

    # FRONT BACKGROUND IMAGE - WITH NO DRAWING SURFACE
    if not shape_selected:
        front_BG_image = pygame.image.load(Path(BACKGROUND_DIRECTORY, 'front_BG.bmp')).convert()
    if shape_selected:
        front_BG_image = pygame.image.load(Path(BACKGROUND_DIRECTORY, 'selected', shape_selected)).convert()
    front_BG_image_width = int(front_BG_image.get_width() / SCALE)
    front_BG_image_height = int(front_BG_image.get_height() / SCALE)
    front_BG_image_scaled = pygame.transform.scale(front_BG_image, (front_BG_image_width, front_BG_image_height))
    front_BG_image_scaled.set_colorkey((0, 0, 0))

    # CURRENT CURSOR COORDINATES
    x_coord, y_coord = pygame.mouse.get_pos()

    # CURSOR POSITION VALIDATIONS
    cursor_over_drawing_surface = x_coord in DRAWING_SURFACE['x'] and y_coord in DRAWING_SURFACE['y']
    cursor_over_circle_shape = x_coord in CIRCLE_SHAPE_SELECT['x'] and y_coord in CIRCLE_SHAPE_SELECT['y']
    cursor_over_square_shape = x_coord in SQUARE_SHAPE_SELECT['x'] and y_coord in SQUARE_SHAPE_SELECT['y']
    
    cursor_over_objects = cursor_over_circle_shape or cursor_over_square_shape
    # print(x_coord, y_coord)

    # CURSOR IMAGE COORDINATES 
    if shape_selected:
        cursor_image = pygame.image.load(Path(SHAPES_DIRECTORY, shape_selected)).convert()
        cursor_image.set_colorkey(BLACK)
        cursor_img_width = cursor_image.get_width()
        cursor_img_height = cursor_image.get_height()
        cursor_with_image_position = (x_coord - cursor_img_width/2, y_coord - cursor_img_height/2)

    # STANDARD CURSOR TYPE CHANGE OVER SHAPES SELECTION
    if cursor_over_objects:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor()

    # DRAWING & SAVING THE MODIFIED BG IMAGE
    if pygame.mouse.get_pressed()[0] == True:
        if shape_selected and cursor_over_drawing_surface:
            if shape_selected == 'circle.bmp':
                pygame.draw.circle(screen, (GREY), (x_coord, y_coord), CIRCLE_SIZE)
            elif shape_selected == 'square.bmp':
                pygame.draw.rect(screen, (GREY), [cursor_with_image_position[0], cursor_with_image_position[1], SQUARE_SIZE, SQUARE_SIZE], 0)
            pygame.image.save(screen, BG_TEMP_PATH)
            BG_image_scaled = pygame.image.load(BG_TEMP_PATH).convert()
            screen.blit(BG_image_scaled, (0,0))

    # DISPLAY THE CURSOR IMAGE(if selected) 
    # & DISPLAY THE BG (the previously modified if drawing already actioned)
    if pygame.mouse.get_pressed()[0] == False:
        screen.blit(BG_image_scaled, (0,0))
        if shape_selected and cursor_over_drawing_surface:
            screen.blit(cursor_image, cursor_with_image_position)

    # DISPLAY THE FRONT/FRAME IMAGE - WITH NO DRAWING SURFACE
    screen.blit(front_BG_image_scaled, (0,0))

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False

        # SHAPES PICKUP RULES
        # YOU HAVE TO PUT BACK THE CURRENT ONE BEFORE USING ANOTHER ONE    
        if event.type == pygame.MOUSEBUTTONDOWN:
            # CIRCLE
            if cursor_over_circle_shape:
                if circle_selected:
                    shape_selected = None
                    counter_circle += 1
                if not circle_selected and not shape_selected:
                    shape_selected = 'circle.bmp'
                    counter_circle += 1
            # SQUARE
            if cursor_over_square_shape:
                if square_selected:
                    shape_selected = None
                    counter_square += 1
                if not square_selected and not shape_selected:
                    shape_selected = 'square.bmp'
                    counter_square += 1

    pygame.display.update()
    clock.tick(60)
 
pygame.quit()