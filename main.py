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


SIZE = 30
shape_size_dict = {
    'circle.bmp': SIZE,
    'square.bmp': SIZE * 1.8,
    'star.bmp': SIZE
    }

CIRCLE_SIZE = shape_size_dict['circle.bmp']
SQUARE_SIZE = shape_size_dict['square.bmp']

# cursor_selected = 'circle.bmp'
# cursor_selected = 'square.bmp'
cursor_selected = None

## CURSOR / SURFACE MAP
# DRAWING SURFACE
DRAWING_SURFACE_X = range(210, 670)
DRAWING_SURFACE_Y = range(105, 430)
# SHAPE SELECTION
# CIRCLE
CIRCLE_SHAPE_SELECT_X = range(110, 170)
CIRCLE_SHAPE_SELECT_Y = range(110, 170)
# SQUARE
SQUARE_SHAPE_SELECT_X = range(80, 130)
SQUARE_SHAPE_SELECT_Y = range(190, 250)
# SHAPE SELECTED/DESELECTED COUNTER
counter_circle, counter_square = [1, 1]
circle_selected = counter_circle % 2 == 0
square_selected = counter_square % 2 == 0

pygame.init()

# GENERATING SHAPES - IF SIZE CHANGES
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

# SCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Magnetic Drawing Board')

# BACKGROUND IMAGE
SCALE = 1.8
BG_image = pygame.image.load(Path(WORKING_DIRECTORY, 'docs', 'skin', 'background', 'BG.jpg')).convert()
BG_image_width = int(BG_image.get_width() / SCALE)
BG_image_height = int(BG_image.get_height() / SCALE)
BG_image_scaled = pygame.transform.scale(BG_image, (BG_image_width, BG_image_height))

run = True
while run:
    # FRONT BACKGROUND IMAGE - WITH NO DRAWING SURFACE
    if not cursor_selected:
        front_BG_image = pygame.image.load(Path(BACKGROUND_DIRECTORY, 'front_BG.bmp')).convert()
    if cursor_selected:
        front_BG_image = pygame.image.load(Path(BACKGROUND_DIRECTORY, 'selected', cursor_selected)).convert()
    front_BG_image_width = int(front_BG_image.get_width() / SCALE)
    front_BG_image_height = int(front_BG_image.get_height() / SCALE)
    front_BG_image_scaled = pygame.transform.scale(front_BG_image, (front_BG_image_width, front_BG_image_height))
    front_BG_image_scaled.set_colorkey((0, 0, 0))

    # CURRENT CURSOR COORDINATES
    x_coord, y_coord = pygame.mouse.get_pos()

    # CURSOR POSITION VALIDATIONS
    cursor_over_drawing_surface = x_coord in DRAWING_SURFACE_X and y_coord in DRAWING_SURFACE_Y
    cursor_over_circle_shape = x_coord in CIRCLE_SHAPE_SELECT_X and y_coord in CIRCLE_SHAPE_SELECT_Y
    cursor_over_square_shape = x_coord in SQUARE_SHAPE_SELECT_X and y_coord in SQUARE_SHAPE_SELECT_Y
    
    cursor_over_objects = cursor_over_circle_shape or cursor_over_square_shape
    # print(x_coord, y_coord)

    # CURSOR IMAGE COORDINATES 
    if cursor_selected:
        cursor_image = pygame.image.load(Path(SHAPES_DIRECTORY, cursor_selected)).convert()
        cursor_image.set_colorkey(BLACK)
        cursor_img_width = cursor_image.get_width()
        cursor_img_height = cursor_image.get_height()
        cursor_with_image_position = (x_coord - cursor_img_width/2, y_coord - cursor_img_height/2)

    # CURSOR TYPE CHANGE OVER SHAPES SELECTION
    if cursor_over_objects:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor()

    # DRAWING & SAVING THE MODIFIED BG IMAGE
    if pygame.mouse.get_pressed()[0] == True:
        if cursor_selected and cursor_over_drawing_surface:
            if cursor_selected == 'circle.bmp':
                pygame.draw.circle(screen, (GREY), (x_coord, y_coord), CIRCLE_SIZE)
            elif cursor_selected == 'square.bmp':
                pygame.draw.rect(screen, (GREY), [cursor_with_image_position[0], cursor_with_image_position[1], SQUARE_SIZE, SQUARE_SIZE], 0)
            pygame.image.save(screen, BG_TEMP_PATH)
            BG_image_scaled = pygame.image.load(BG_TEMP_PATH).convert()
            screen.blit(BG_image_scaled, (0,0))
        if cursor_over_circle_shape:
            cursor_selected = 'circle.bmp'
        if cursor_over_square_shape:
            cursor_selected = 'square.bmp'

    # DISPLAY THE CURSOR IMAGE(if selected) 
    # & DISPLAY THE BG (the previously modified if drawing already actioned)
    if pygame.mouse.get_pressed()[0] == False:
        screen.blit(BG_image_scaled, (0,0))
        if cursor_selected and cursor_over_drawing_surface:
            screen.blit(cursor_image, cursor_with_image_position)

    # DISPLAY THE FRONT/FRAME IMAGE - WITH NO DRAWING SURFACE
    screen.blit(front_BG_image_scaled, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
   
    pygame.display.update()
 
pygame.quit()