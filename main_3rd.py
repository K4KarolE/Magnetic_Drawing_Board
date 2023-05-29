import pygame
from pathlib import Path
import os

#SCREEN
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# PATHS
WORKING_DIRECTORY = Path(os.path.dirname(__file__), 'docs', 'skin', 'classic')
DRAWING_DIRECTORY = Path(WORKING_DIRECTORY, 'drawing')
OBJECTS_DIRECTORY = Path(WORKING_DIRECTORY, 'objects')
BACKGROUND_DIRECTORY = Path(WORKING_DIRECTORY, 'background')

''' -- PYGAME -- '''
pygame.init()
clock = pygame.time.Clock()

# SCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Magnetic Drawing Board')


def display_object(image_name, directory, file_name, x_coord=0, y_coord=0, scale=1, opacity=255):
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


# DRAWING SURFACE IMAGE
DRAWING_SURFACE = display_object('DRAWING_SURFACE', BACKGROUND_DIRECTORY, 'drawing_surface.png')[0]
DRAWING_SURFACE_RECT = pygame.Rect((171+30, 121+30), (833-30, 509-30))  # Rect(left, top, width, height)

# GRID
GRID = display_object('BACKGROUND_IMAGE', BACKGROUND_DIRECTORY, 'grid.png', 0, 0, 4, 10)[0] # coord, coord, scale, opacity(0-255) // [0] RECT will not be used

# BACKGROUND IMAGE
BACKGROUND = display_object('BACKGROUND_IMAGE', BACKGROUND_DIRECTORY, 'background.png')[0]

# ERASER
ERASER, ERASER_RECT = display_object('SQUARE', OBJECTS_DIRECTORY, 'eraser.png', 153, 668)

## SHAPES
SHAPES_X_COORD = 98
# CIRCLE
CIRCLE, CIRCLE_RECT = display_object('CIRCLE', OBJECTS_DIRECTORY, 'circle.png', SHAPES_X_COORD, 242)
# SQUARE
SQUARE, SQUARE_RECT = display_object('SQUARE', OBJECTS_DIRECTORY, 'square.png', SHAPES_X_COORD, 350)
# TRIANGLE
TRIANGLE, TRIANGLE_RECT = display_object('SQUARE', OBJECTS_DIRECTORY, 'triangle.png', SHAPES_X_COORD, 465)


SHAPES = {
    'circle': {
        'image': CIRCLE, 
        'image_rect': CIRCLE_RECT,
        'drawing_file': 'circle.png',
        'drawing_image': None,
        'cursor': None,
        'cursor_size': None, 
        'selected':False,
        'counter': 1 }, 
    'square': {
        'image': SQUARE, 
        'image_rect':SQUARE_RECT, 
        'drawing_file': 'square.png',
        'drawing_image': None,
        'cursor': None,
        'cursor_size': None, 
        'selected':False,
        'counter': 1}, 
    'triangle': {
        'image': TRIANGLE, 
        'image_rect':TRIANGLE_RECT,
        'drawing_file': 'triangle.png',
        'drawing_image': None, 
        'cursor': None,
        'cursor_size': None, 
        'selected':False,
        'counter': 1}
    }

OBJECT_RECT_LIST = []
for shape in SHAPES.values():
    # CURSOR IMAGES
    image_size = int(shape['image'].get_width())
    shape['cursor_size'] = image_size
    surf = pygame.Surface((image_size, image_size), pygame.SRCALPHA)
    surf.blit(shape['image'], (0,0))
    shape['cursor'] = pygame.cursors.Cursor((int(image_size/2), int(image_size/2)), surf)
    # DRAWING IMAGES
    shape['drawing_image'] = display_object('DRAWING_IMAGE', DRAWING_DIRECTORY, shape['drawing_file'], 0, 0, 0.65)[0]  # [0] - just the image no RECT
    # RECT LIST
    OBJECT_RECT_LIST.append(shape['image_rect'])

OBJECT_RECT_LIST.append(ERASER_RECT)

''' -- LOOP -- '''
run = True
eraser_moving = False
a_shape_selected = False
drawing_shape = None
while run:
    cursor_coord_x, cursor_coord_y = pygame.mouse.get_pos()
    # print(cursor_coord_x, cursor_coord_y)

    # CURSOR
    if a_shape_selected == False:
        if OBJECT_RECT_LIST[0].collidepoint(cursor_coord_x, cursor_coord_y):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif OBJECT_RECT_LIST[1].collidepoint(cursor_coord_x, cursor_coord_y):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif OBJECT_RECT_LIST[2].collidepoint(cursor_coord_x, cursor_coord_y):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif OBJECT_RECT_LIST[3].collidepoint(cursor_coord_x, cursor_coord_y):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor()

    # DRAWING
    if pygame.mouse.get_pressed()[0] == True and DRAWING_SURFACE_RECT.collidepoint(event.pos) and a_shape_selected:
        DRAWING_SURFACE.blit(drawing_shape, (cursor_coord_x-drawing_corigation, cursor_coord_y-drawing_corigation))

    # EVENTS
    for event in pygame.event.get():

        # MOUSEBUTTONDOWN
        if event.type == pygame.MOUSEBUTTONDOWN:
            # SHAPES
            for shape in SHAPES.values():
                if shape['image_rect'].collidepoint(event.pos):
                    # SHAPE SELECTION COUNTER
                    shape['counter'] +=1
                    # SELECT THE SHAPE
                    if shape['counter']%2==0 and a_shape_selected == False:
                        a_shape_selected = True
                        pygame.mouse.set_cursor(shape['cursor'])
                        shape['selected'] = True     # shape image will not be displayed -> cursor will have the shape image
                        drawing_shape = shape['drawing_image']
                        drawing_corigation = int(shape['cursor_size'] / 2)
                    # DESELECT THE SHAPE
                    elif shape['selected']:          # shape image not displayed = that is the selected one -> able to "put back"
                        a_shape_selected = False
                        pygame.mouse.set_cursor()
                        shape['selected'] = False
                        drawing_shape = None
            # ERASER          
            if ERASER_RECT.collidepoint(event.pos):
                eraser_moving = True

        # MOUSEMOTION
        elif event.type == pygame.MOUSEMOTION and eraser_moving and a_shape_selected == False:
            if 160 < cursor_coord_x < SCREEN_WIDTH - 160:
                # MOVE ERASER
                ERASER_RECT.move_ip(event.rel[0], 0)    # no vertical movement allowed
                # DRAW RECT./ERASE SURFACE
                pygame.draw.rect(DRAWING_SURFACE, ('White'), [cursor_coord_x-20, 120, 50, 540], 0)

        # MOUSEBUTTONUP
        elif event.type == pygame.MOUSEBUTTONUP:
            eraser_moving = False

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
    # SHAPES
    for shape in SHAPES.values():
        if shape['selected'] == False:
            screen.blit(shape['image'], shape['image_rect'])

    # ERASER
    screen.blit(ERASER, ERASER_RECT)

    pygame.display.update()
    clock.tick(60)
 
pygame.quit()