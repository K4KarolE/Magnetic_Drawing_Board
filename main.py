''' SKIN: MINIMAL '''

import pygame
from pathlib import Path
import os

#SCREEN
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# SKIN
SKINS = ['classic', 'minimal']

def main(skin_selected = 'minimal'):
    # PATHS
    CURRENT_DIRECTORY = os.path.dirname(__file__)
    WORKING_DIRECTORY = Path(CURRENT_DIRECTORY, 'docs', 'skin', skin_selected)
    DRAWING_DIRECTORY = Path(WORKING_DIRECTORY, 'drawing')
    OBJECTS_DIRECTORY = Path(WORKING_DIRECTORY, 'objects')
    BACKGROUND_DIRECTORY = Path(WORKING_DIRECTORY, 'background')

    ''' -- PYGAME -- '''
    pygame.init()
    clock = pygame.time.Clock()

    # SCREEN
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Magnetic Drawing Board')

    def capture_screen():
            sub = DRAWING_SURFACE.subsurface(DRAWING_SURFACE_RECT)
            sub = screen
            pygame.image.save(sub, Path(CURRENT_DIRECTORY, 'screenshot', 'screenshot.png'))


    def generate_asset(image_name, directory, file_name, x_coord=0, y_coord=0, scale=1, opacity=255):
        image_name = pygame.image.load(Path(directory, file_name)).convert_alpha()
        if scale != 1:
            image_name_width = int(image_name.get_width() / scale)
            image_name_height = int(image_name.get_height() / scale)
            image_name = pygame.transform.scale(image_name, (image_name_width, image_name_height))
        if opacity != 255:
            image_name.set_alpha(opacity)
        image_name_rect = image_name.get_rect()
        image_name_rect.center = x_coord, y_coord
        return image_name, image_name_rect


    # DRAWING SURFACE IMAGE
    DRAWING_SURFACE = generate_asset('DRAWING_SURFACE', BACKGROUND_DIRECTORY, 'drawing_surface.png')[0]
    DRAWING_SURFACE_RECT = pygame.Rect((171, 121), (900, 500))  # Rect(left, top, width, height)

    # GRID
    GRID = generate_asset('BACKGROUND_IMAGE', BACKGROUND_DIRECTORY, 'grid.png', 0, 0, 4, 6)[0] # coord, coord, scale, opacity(0-255) // [0] RECT will not be used

    # BACKGROUND IMAGE
    BACKGROUND = generate_asset('BACKGROUND_IMAGE', BACKGROUND_DIRECTORY, 'background.png')[0]

    # ERASER
    ERASER, ERASER_RECT = generate_asset('SQUARE', OBJECTS_DIRECTORY, 'eraser.png', 160, 680)

    ## SHAPES
    SHAPES_X_COORD = 87
    SHAPES_Y_COORD = 250
    CORRRECTION = 107
    # CIRCLE
    CIRCLE, CIRCLE_RECT = generate_asset('CIRCLE', OBJECTS_DIRECTORY, 'circle.png', SHAPES_X_COORD, SHAPES_Y_COORD)
    # SQUARE
    SQUARE, SQUARE_RECT = generate_asset('SQUARE', OBJECTS_DIRECTORY, 'square.png', SHAPES_X_COORD - 1, SHAPES_Y_COORD + CORRRECTION + 2)
    # TRIANGLE
    TRIANGLE, TRIANGLE_RECT = generate_asset('SQUARE', OBJECTS_DIRECTORY, 'triangle.png', SHAPES_X_COORD, SHAPES_Y_COORD +CORRRECTION * 2 + 2)
    # PEN
    PEN, PEN_RECT = generate_asset('PEN', OBJECTS_DIRECTORY, 'pen.png', 1131, 374, 3)
    # PEN ACTIVE
    PEN_ACTIVE = generate_asset('PEN_ACTIVE', OBJECTS_DIRECTORY, 'pen_active.png', 0, 0, 3)[0]

    SHAPES = {
        'circle': {
            'image': CIRCLE, 
            'image_rect': CIRCLE_RECT,
            'drawing_file': 'circle.png',
            'drawing_image': None,
            'rotation': 0,
            'cursor': None,
            'cursor_size': None, 
            'selected':False,
            'counter': 1 }, 
        'square': {
            'image': SQUARE, 
            'image_rect':SQUARE_RECT, 
            'drawing_file': 'square.png',
            'drawing_image': None,
            'drawing_image_rotated': None,
            'rotation': 0,
            'cursor': None,
            'cursor_size': None, 
            'selected':False,
            'counter': 1}, 
        'triangle': {
            'image': TRIANGLE, 
            'image_rect': TRIANGLE_RECT,
            'drawing_file': 'triangle.png',
            'drawing_image': None,
            'drawing_image_rotated': None,
            'rotation': 0,
            'cursor': None,
            'cursor_size': None, 
            'selected':False,
            'counter': 1},
        'pen': {
            'image': PEN, 
            'image_rect': PEN_RECT,
            'drawing_file': 'pen.png',
            'drawing_image': None,
            'rotation': 0, 
            'cursor': None,
            'cursor_size': None, 
            'selected':False,
            'counter': 1}
        }

    OBJECT_RECT_LIST = []

    # GENERATE CURSOR / DRAWING IMAGES
    for shape in SHAPES.values():
        # CURSOR IMAGES
        if shape['image'] == PEN:
            image = PEN_ACTIVE
        else:
            image = shape['image']
        image_width, image_height = image.get_size()
        shape['cursor_size'] = [image_width, image_height]
        surf = pygame.Surface((image_width, image_height), pygame.SRCALPHA)
        surf.blit(image, (0,0))
        if image == PEN_ACTIVE:
            shape['cursor'] = pygame.cursors.Cursor((0, image_height-18), surf)   # cursor bottom left corner
        else:
            shape['cursor'] = pygame.cursors.Cursor((int(image_width/2), int(image_height/2)), surf)   # cursor in the middle
        # DRAWING IMAGES
        shape['drawing_image'] = generate_asset('DRAWING_IMAGE', DRAWING_DIRECTORY, shape['drawing_file'])[0]  # [0] - just the image no RECT
        # RECT LIST
        OBJECT_RECT_LIST.append(shape['image_rect'])

    OBJECT_RECT_LIST.append(ERASER_RECT)

    def rotate_images(shape, cursor_rotation):
        # CURSOR
        image_rotated = pygame.transform.rotate(shape['image'], cursor_rotation)
        image_width, image_height = image_rotated.get_size()
        shape['cursor_size'] = [image_width, image_height]
        surf = pygame.Surface((image_width, image_height), pygame.SRCALPHA)
        surf.blit(image_rotated, (0,0))
        shape['cursor'] = pygame.cursors.Cursor((int(image_width/2), int(image_height/2)), surf)
        # DRAWING IMAGE
        shape['drawing_image_rotated'] = pygame.transform.rotate(shape['drawing_image'], cursor_rotation)

    ''' -- LOOP -- '''
    run = True
    eraser_moving = False
    a_shape_selected = False
    drawing_shape = None
    while run:
        cursor_coord_x, cursor_coord_y = pygame.mouse.get_pos()
        # print(cursor_coord_x, cursor_coord_y)

        # CURSOR OVER OBJECTS
        if a_shape_selected == False:
            # CIRCLE
            if OBJECT_RECT_LIST[0].collidepoint(cursor_coord_x, cursor_coord_y):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            # SQUARE
            elif OBJECT_RECT_LIST[1].collidepoint(cursor_coord_x, cursor_coord_y):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            # TRIANGLE
            elif OBJECT_RECT_LIST[2].collidepoint(cursor_coord_x, cursor_coord_y):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            # PEN
            elif OBJECT_RECT_LIST[3].collidepoint(cursor_coord_x, cursor_coord_y):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            # ERASER
            elif OBJECT_RECT_LIST[4].collidepoint(cursor_coord_x, cursor_coord_y):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor()
        
        # DRAWING
        if pygame.mouse.get_pressed()[0] == True and DRAWING_SURFACE_RECT.collidepoint(event.pos) and a_shape_selected:
            DRAWING_SURFACE.blit(drawing_shape, (cursor_coord_x-drawing_corigation_x, cursor_coord_y-drawing_corigation_y))

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
                            # DRAWING CORIGATION - CURSOR POSITION VS CURSOR IMAGE
                            if shape['image'] == PEN:
                                drawing_corigation_x = 0 # + 5    # drawing in the top left of the PEN cursor image
                                drawing_corigation_y = 0 #-shape['cursor_size'][1] + 10
                            else:    
                                drawing_corigation_x = int(shape['cursor_size'][0] / 2)     # drawing in middle of the cursor image
                                drawing_corigation_y = int(shape['cursor_size'][1] / 2)
                        # DESELECT THE SHAPE
                        elif shape['selected']:          # shape image not displayed = that is the selected one -> able to "put back"
                            a_shape_selected = False
                            pygame.mouse.set_cursor()
                            shape['selected'] = False
                            drawing_shape = None
                            # BACK TO ORIGINAL, NON-ROTATED POSITION
                            if shape['rotation'] != 0:
                                shape['rotation'] = 0
                                rotate_images(shape, shape['rotation'])

                    # IMAGE ROTATION
                    if shape['selected'] and shape['image'] != PEN and shape['image'] != CIRCLE:
                        # TO ROTATE LEFT - MIDDLE MOUSE BUTTON
                        if pygame.mouse.get_pressed()[1] == True:                       
                            shape['rotation'] += 10
                            # UPDATE CURSOR, DRAWING IMAGE
                            rotate_images(shape, shape['rotation'])
                            drawing_shape = shape['drawing_image_rotated']
                            drawing_corigation_x = int(shape['cursor_size'][0] / 2)     
                            drawing_corigation_y = int(shape['cursor_size'][1] / 2)
                            pygame.mouse.set_cursor(shape['cursor'])
            
                        # TO ROTATE RIGHT - RIGHT MOUSE BUTTON
                        elif pygame.mouse.get_pressed()[2] == True:
                            shape['rotation'] -= 10
                            # UPDATE CURSOR, DRAWING IMAGE
                            rotate_images(shape, shape['rotation'])
                            drawing_shape = shape['drawing_image_rotated']
                            drawing_corigation_x = int(shape['cursor_size'][0] / 2)     
                            drawing_corigation_y = int(shape['cursor_size'][1] / 2)
                            pygame.mouse.set_cursor(shape['cursor'])
                        
                # ERASER          
                if ERASER_RECT.collidepoint(event.pos):
                    eraser_moving = True

            # MOUSEMOTION
            elif event.type == pygame.MOUSEMOTION and eraser_moving and a_shape_selected == False:
                if 160 < cursor_coord_x < SCREEN_WIDTH - 130:
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

if __name__ == '__main__': 
    main()