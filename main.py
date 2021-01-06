import pygame
from pygame.locals import *
import time
import player

pygame.init()
clock = pygame.time.Clock()

screenWidth = 1000
screenHeight = 500

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Weirdo")

screen.fill((0,0,0))

ground=pygame.image.load('ground.png')

player = player.Player()

run = True
while run:
    clock.tick(60) #fps
    screen.fill((0, 0, 0))
    screen.blit(ground, (0, screenHeight/2-(ground.get_height()/2)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
            #sys.exit()

    player.update()

    pygame.display.update()