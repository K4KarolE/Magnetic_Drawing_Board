import pygame
from pathlib import Path
import os

# COLORS
COLOR = 'Grey'
ERASER_COLOR = 'White'

#SCREEN
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# PATHS
WORKING_DIRECTORY = Path(os.path.dirname(__file__), 'docs', 'skin', 'classic')

SHAPES_DIRECTORY = Path(WORKING_DIRECTORY, 'shapes')
BACKGROUND_DIRECTORY = Path(WORKING_DIRECTORY, 'background')
OBJECTS_DIRECTORY = Path(WORKING_DIRECTORY, 'objects')



''' -- PYGAME -- '''
pygame.init()
clock = pygame.time.Clock()

# SCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Magnetic Drawing Board')


def display_surface(image_name, directory, file_name, scale=1, opacity=255):
    image_name = pygame.image.load(Path(directory, file_name)).convert()
    if scale != 1:
        image_name_width = int(image_name.get_width() / scale)
        image_name_height = int(image_name.get_height() / scale)
        image_name = pygame.transform.scale(image_name, (image_name_width, image_name_height))
    if opacity != 255:
        image_name.set_alpha(opacity)
    image_name.set_colorkey('Black')
    return image_name

def display_object(image_name, directory, file_name, x_coord, y_coord, scale=1, opacity=255):
    image_name = pygame.image.load(Path(directory, file_name)).convert()
    if scale != 1:
        image_name_width = int(image_name.get_width() / scale)
        image_name_height = int(image_name.get_height() / scale)
        image_name = pygame.transform.scale(image_name, (image_name_width, image_name_height))
    if opacity != 255:
        image_name.set_alpha(opacity)
    image_name.set_colorkey('Black')
    image_name_rect = image_name.get_rect()
    image_name_rect.center = x_coord, y_coord
    return image_name, image_name_rect


## DISPLAY SURFACE
# DRAWING SURFACE IMAGE
DRAWING_SURFACE = display_surface('DRAWING_SURFACE', BACKGROUND_DIRECTORY, 'drawing_surface.png')

# # GRID
GRID = display_surface('BACKGROUND_IMAGE', BACKGROUND_DIRECTORY, 'grid.png', 4, 10)

# BACKGROUND IMAGE
BACKGROUND = display_surface('BACKGROUND_IMAGE', BACKGROUND_DIRECTORY, 'background.png')

## DISPLAY OBJECTS
# CIRCLE
CIRCLE, CIRCLE_RECT = display_object('CIRCLE', OBJECTS_DIRECTORY, 'circle.png', 30, 60)

# SQUARE
SQUARE, SQUARE_RECT = display_object('SQUARE', OBJECTS_DIRECTORY, 'square.png', 30, 150)

# TRIANGLE
TRIANGLE, TRIANGLE_RECT = display_object('SQUARE', OBJECTS_DIRECTORY, 'triangle.png', 30, 260)



''' LOOP '''
run = True
eraser_moving = False
while run:
    for event in pygame.event.get():
    









        # QUIT
        if event.type == pygame.QUIT:
            run = False
    
    # DISPLAY DRAWING SURFACE
    screen.blit(DRAWING_SURFACE, (0,0))

    # DISPLAY GRID ON THE DRAWING SURFACE
    DRAWING_SURFACE.blit(GRID, (0,0))

    # DISPLAY BACKGOUND
    screen.blit(BACKGROUND, (0,0))

    ## DISPLAY OBJECTS
    # CIRCLE
    screen.blit(CIRCLE, CIRCLE_RECT)

    # SQUARE
    screen.blit(SQUARE, SQUARE_RECT)

    # TRIANGLE
    screen.blit(TRIANGLE, TRIANGLE_RECT)

    pygame.display.update()
    clock.tick(60)
 
pygame.quit()