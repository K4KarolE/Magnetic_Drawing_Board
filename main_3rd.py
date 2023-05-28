import pygame
from pathlib import Path
import os

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
SHAPES_X_COORD = 98
# CIRCLE
CIRCLE, CIRCLE_RECT = display_object('CIRCLE', OBJECTS_DIRECTORY, 'circle.png', SHAPES_X_COORD, 242)
# SQUARE
SQUARE, SQUARE_RECT = display_object('SQUARE', OBJECTS_DIRECTORY, 'square.png', SHAPES_X_COORD, 350)
# TRIANGLE
TRIANGLE, TRIANGLE_RECT = display_object('SQUARE', OBJECTS_DIRECTORY, 'triangle.png', SHAPES_X_COORD, 465)


SHAPES = {
    'circle': [CIRCLE, CIRCLE_RECT, 'cursor', False],
    'square': [SQUARE, SQUARE_RECT, 'cursor', False],
    'triangle': [TRIANGLE, TRIANGLE_RECT, 'cursor', False]
    }

## CURSOR IMAGES
for shape in SHAPES.values():
    surf = pygame.Surface((80, 80), pygame.SRCALPHA)
    surf.blit(shape[0], (0,0))
    shape[2] = pygame.cursors.Cursor((40, 40), surf)


''' LOOP '''
run = True
moving = False
while run:
    # print(pygame.mouse.get_pos())

    for event in pygame.event.get():

        # MOUSEBUTTONDOWN
        if event.type == pygame.MOUSEBUTTONDOWN:

            for shape in SHAPES.values():
                if shape[1].collidepoint(event.pos):
                    pygame.mouse.set_cursor(shape[2])
                    shape[3] = True
            moving = True
    
        # # MOUSEMOTION
        # elif event.type == pygame.MOUSEMOTION and moving:
        #     selected_object.move_ip(event.rel)

        # MOUSEBUTTONUP
        elif event.type == pygame.MOUSEBUTTONUP:
            moving = False

        # QUIT
        elif event.type == pygame.QUIT:
            run = False
    
    # DISPLAY DRAWING SURFACE
    screen.blit(DRAWING_SURFACE, (0,0))

    # DISPLAY GRID ON THE DRAWING SURFACE
    DRAWING_SURFACE.blit(GRID, (0,0))

    # DISPLAY BACKGOUND
    screen.blit(BACKGROUND, (0,0))

    ## DISPLAY OBJECTS
    for shape in SHAPES.values():
        if shape[3] == False:
            screen.blit(shape[0], shape[1])     # (image, image_rect)

    pygame.display.update()
    clock.tick(60)
 
pygame.quit()