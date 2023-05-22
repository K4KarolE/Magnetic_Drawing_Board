import pygame

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Magnetic Drawing Board')
screen.fill((255,255,255))


run = True
while run:

    # DRAWING
    if pygame.mouse.get_pressed()[0] == True:
        x_cord, y_cord = pygame.mouse.get_pos()
        pygame.draw.circle(screen, (0,255,255,100), (x_cord, y_cord), 30)

    # ERASER
    if pygame.mouse.get_pressed()[2] == True:
        x_cord, y_cord = pygame.mouse.get_pos()
        pygame.draw.circle(screen, (255,255,255,255), (x_cord, y_cord), 30)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.flip()