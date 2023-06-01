'''
def capture_screen():
    sub = DRAWING_SURFACE.subsurface(DRAWING_SURFACE_RECT)  / specific part of the screen
    sub = screen                                            / the whole screen
    pygame.image.save(sub, Path(CURRENT_DIRECTORY, 'screenshot', 'screenshot.png'))
'''