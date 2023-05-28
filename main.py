import pygame
from pathlib import Path
import os

# COLORS
COLOR = 'Grey'
ERASER_COLOR = 'White'

#SCREEN
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# PATHS
WORKING_DIRECTORY = os.path.dirname(__file__)
SHAPES_DIRECTORY = Path(WORKING_DIRECTORY, 'docs', 'skin', 'shapes')
BACKGROUND_DIRECTORY = Path(WORKING_DIRECTORY, 'docs', 'skin', 'background')
PICTURES_DIRECTORY = Path(WORKING_DIRECTORY, 'docs', 'skin', 'pictures')

# SHAPES AND SIZES
SIZE = 30
shape_size_dict = {
    'circle.bmp': SIZE,
    'square.bmp': SIZE * 1.8,
    'pen.bmp': SIZE / 3,
    'triangle.bmp': SIZE
    }
shape_selected = None

CIRCLE_SIZE = shape_size_dict['circle.bmp']
SQUARE_SIZE = shape_size_dict['square.bmp']
PEN_SIZE = shape_size_dict['pen.bmp']
TRIANGLE_SIZE = shape_size_dict['triangle.bmp']

cursor_rotation = 0 

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
# PEN - SHAPE SELECTION
PEN_SHAPE_SELECT = {
    'x': range(690, 780),
    'y': range(225, 450)
    }
# TRIANGLE - SHAPE SELECTION
TRIANGLE_SHAPE_SELECT = {
    'x': range(65, 110),
    'y': range(230, 300)
    }

# SHAPE SELECTED/DESELECTED COUNTER
counter_circle, counter_square, counter_pen, counter_triangle  = [1, 1, 1, 1]

''' -- PYGAME -- '''
pygame.init()
clock = pygame.time.Clock()

# GENERATING SHAPES - IF SIZE CHANGES
def generating_shapes():

    shape_list = os.listdir(SHAPES_DIRECTORY)

    for item in shape_list:
        if pygame.image.load(Path(SHAPES_DIRECTORY, item)).get_width() != shape_size_dict[item]:
            # CIRCLE
            if item == 'circle.bmp':
                SIDE = CIRCLE_SIZE * 2    # just for the 'screen_shape' screen -> to generate new image
                screen_shape = pygame.display.set_mode((SIDE, SIDE))
                screen_shape.fill('Black')
                pygame.draw.circle(screen_shape, (COLOR), (SIDE/2, SIDE/2), CIRCLE_SIZE)
                pygame.image.save(screen_shape, Path(SHAPES_DIRECTORY, 'circle.bmp'))
            # SQUARE
            if item == 'square.bmp':
                screen_shape = pygame.display.set_mode((SQUARE_SIZE, SQUARE_SIZE))
                screen_shape.fill('Black')
                pygame.draw.rect(screen_shape, (COLOR), [0, 0, SQUARE_SIZE, SQUARE_SIZE], 0)
                pygame.image.save(screen_shape, Path(SHAPES_DIRECTORY, 'square.bmp'))
            # PEN
            if item == 'pen.bmp':
                SIDE = PEN_SIZE * 2
                screen_shape = pygame.display.set_mode((SIDE, SIDE))
                screen_shape.fill('Black')
                pygame.draw.circle(screen_shape, (COLOR), (SIDE/2, SIDE/2), PEN_SIZE)
                pygame.image.save(screen_shape, Path(SHAPES_DIRECTORY, 'pen.bmp'))
            # TRIANGLE
            if item == 'triangle.bmp':
                SIDE = TRIANGLE_SIZE * 2
                screen_shape = pygame.display.set_mode((SIDE, SIDE))
                screen_shape.fill('Black')
                pygame.draw.polygon(screen_shape, (COLOR), ((TRIANGLE_SIZE, 0), (SIDE, SIDE), (0, SIDE)))
                pygame.image.save(screen_shape, Path(SHAPES_DIRECTORY, 'triangle.bmp'))

generating_shapes()


# SCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Magnetic Drawing Board')

# DRAWING SURFACE IMAGE
SCALE = 1.8
drawing_surface_image = pygame.image.load(Path(BACKGROUND_DIRECTORY, 'BG.png')).convert()
drawing_surface_image_width = int(drawing_surface_image.get_width() / SCALE)
drawing_surface_image_height = int(drawing_surface_image.get_height() / SCALE)
drawing_surface_image = pygame.transform.scale(drawing_surface_image, (drawing_surface_image_width, drawing_surface_image_height))
drawing_surface_image.set_colorkey('Black')

# GRID IMAGE
SCALE_GRID = 6
GRID_image = pygame.image.load(Path(BACKGROUND_DIRECTORY, 'grid.png')).convert()
GRID_image_width = int(GRID_image.get_width() / SCALE_GRID)
GRID_image_height = int(GRID_image.get_height() / SCALE_GRID)
GRID_image_scaled = pygame.transform.scale(GRID_image, (GRID_image_width, GRID_image_height))
GRID_image_scaled.set_colorkey('Black')
GRID_image_scaled.set_alpha(10)    # opacity 0-255

# ERASER IMAGE
SCALE_ERASER = 2
ERASER_image = pygame.image.load(Path(PICTURES_DIRECTORY, 'eraser.png')).convert()
ERASER_image_width = int(ERASER_image.get_width() / SCALE_ERASER)
ERASER_image_height = int(ERASER_image.get_height() / SCALE_ERASER)
ERASER_image = pygame.transform.scale(ERASER_image, (ERASER_image_width, ERASER_image_height))
ERASER_image.set_colorkey('Black')
ERASER_RECT = ERASER_image.get_rect()
ERASER_RECT.center = 150, 520   # ERASER_image and ERASER_RECT location

''' LOOP '''
run = True
eraser_moving = False
while run:

    # CURSOR IMAGE
    if shape_selected:
        #LOAD
        cursor_image = pygame.image.load(Path(SHAPES_DIRECTORY, shape_selected)).convert()
        cursor_image.set_colorkey('Black')
        # ROTATION
        cursor_image = pygame.transform.rotate(cursor_image, cursor_rotation)
        # GENERATE
        cursor_size = int(cursor_image.get_width())
        cursor_surface = pygame.Surface((cursor_size, cursor_size), pygame.SRCALPHA)
        cursor_surface.blit(cursor_image, (0,0))
        cursor_selected = pygame.cursors.Cursor((int(cursor_size/2), int(cursor_size/2)), cursor_surface)

    # SHAPE SELECTED/DESELECTED COUNTER
    circle_selected = counter_circle % 2 == 0
    square_selected = counter_square % 2 == 0
    pen_selected = counter_pen % 2 == 0
    triangle_selected = counter_triangle % 2 == 0

    # FRONT BACKGROUND IMAGE - WITH NO DRAWING SURFACE
    if not shape_selected:
        front_BG_image = pygame.image.load(Path(BACKGROUND_DIRECTORY, 'front_BG.bmp')).convert()
    if shape_selected:
        front_BG_image = pygame.image.load(Path(BACKGROUND_DIRECTORY, 'selected', shape_selected)).convert()
    front_BG_image_width = int(front_BG_image.get_width() / SCALE)
    front_BG_image_height = int(front_BG_image.get_height() / SCALE)
    front_BG_image = pygame.transform.scale(front_BG_image, (front_BG_image_width, front_BG_image_height))
    front_BG_image.set_colorkey('Black')

    # CURRENT CURSOR COORDINATES
    x_coord, y_coord = pygame.mouse.get_pos()
    # print(x_coord, y_coord)

    # CURSOR POSITION VALIDATIONS
    cursor_over_drawing_surface = x_coord in DRAWING_SURFACE['x'] and y_coord in DRAWING_SURFACE['y']
    cursor_over_circle_shape = x_coord in CIRCLE_SHAPE_SELECT['x'] and y_coord in CIRCLE_SHAPE_SELECT['y']
    cursor_over_square_shape = x_coord in SQUARE_SHAPE_SELECT['x'] and y_coord in SQUARE_SHAPE_SELECT['y']
    cursor_over_pen_shape = x_coord in PEN_SHAPE_SELECT['x'] and y_coord in PEN_SHAPE_SELECT['y']
    cursor_over_triangle_shape = x_coord in TRIANGLE_SHAPE_SELECT['x'] and y_coord in TRIANGLE_SHAPE_SELECT['y']    

    cursor_over_objects = cursor_over_circle_shape or cursor_over_square_shape or cursor_over_pen_shape or cursor_over_triangle_shape

    # STANDARD CURSOR TYPE CHANGE OVER SHAPES SELECTION
    if cursor_over_objects:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif shape_selected and cursor_over_drawing_surface:
        pygame.mouse.set_cursor(cursor_selected)
    elif not cursor_over_objects or not cursor_over_drawing_surface:
        pygame.mouse.set_cursor()

    
    # DRAWING
    if pygame.mouse.get_pressed()[0] == True:
        if shape_selected and cursor_over_drawing_surface:
            drawing_surface_image.blit(cursor_image, (x_coord-int(cursor_size/2), y_coord-int(cursor_size/2)))


# EVENT HANDLING  
    for event in pygame.event.get():
        
        # QUIT
        if event.type == pygame.QUIT:
            run = False

        # MOUSEBUTTONDOWN
        # SHAPES PICKUP RULES
        # YOU HAVE TO PUT BACK THE CURRENT ONE BEFORE USING ANOTHER ONE
        # -> TO AVOID LOSING THE PIECES OF THE BOARD
        elif event.type == pygame.MOUSEBUTTONDOWN:

            ## SHAPE SELECTION RULE
            def shape_selection_rule(individual_shape_selected, shape_selected, counter, shape_image, cursor_rotation):
                if individual_shape_selected:
                    shape_selected = None
                    counter +=1
                    cursor_rotation = 0
                if not individual_shape_selected and not shape_selected:
                    shape_selected = shape_image
                    counter += 1
                return individual_shape_selected, shape_selected, counter, cursor_rotation

            # CIRCLE
            if cursor_over_circle_shape:
                circle_selected, shape_selected, counter_circle, cursor_rotation = shape_selection_rule(circle_selected, shape_selected, counter_circle, 'circle.bmp', cursor_rotation)

            # SQUARE
            elif cursor_over_square_shape:
                square_selected, shape_selected, counter_square, cursor_rotation = shape_selection_rule(square_selected, shape_selected, counter_square, 'square.bmp', cursor_rotation)
            
            # PEN
            elif cursor_over_pen_shape:
                pen_selected, shape_selected, counter_pen, cursor_rotation = shape_selection_rule(pen_selected, shape_selected, counter_pen, 'pen.bmp', cursor_rotation)
     
            # TRIANGLE
            elif cursor_over_triangle_shape:
                triangle_selected, shape_selected, counter_triangle, cursor_rotation = shape_selection_rule(triangle_selected, shape_selected, counter_triangle, 'triangle.bmp', cursor_rotation)


            ## ERASER
            elif ERASER_RECT.collidepoint(event.pos):
                eraser_moving = True

            ## CURSOR ROTATION
            # TO LEFT - MIDDLE MOUSE BUTTON
            elif pygame.mouse.get_pressed()[1] == True:
                cursor_rotation += 10
            # TO RIGHT - RIGHT MOUSE BUTTON
            elif pygame.mouse.get_pressed()[2] == True:
                cursor_rotation -= 10
            
        # MOUSEBUTTONUP
        elif event.type == pygame.MOUSEBUTTONUP:
            eraser_moving = False
        
        # MOUSEMOTION
        elif event.type == pygame.MOUSEMOTION and eraser_moving:
            if 120 < x_coord < SCREEN_WIDTH - 120:
                # MOVE ERASER
                ERASER_RECT.move_ip(event.rel[0], 0)    # no vertical movement
                # DRAW RECT./ERASE SURFACE
                pygame.draw.rect(drawing_surface_image, (ERASER_COLOR), [ x_coord-40, 90, 50, 450], 0)

    # DRAWING SURFACE
    screen.blit(drawing_surface_image, (0,0))

    # GRID
    drawing_surface_image.blit(GRID_image_scaled, (100,80))
    
    # DISPLAY THE FRONT/FRAME IMAGE - WITH NO DRAWING SURFACE
    screen.blit(front_BG_image, (0,0))

    # ERASER IMAGE
    screen.blit(ERASER_image, ERASER_RECT)

    pygame.display.update()
    clock.tick(60)
 
pygame.quit()