import pygame
import math

tile_size = 40
screenH = 500
groundH = 40

class Player():
    def __init__(self):  # jaka postać też?
        self.img_stay = []
        self.img_slide = []
        self.img_run = []
        self.img_jump = []
        self.img_dead = []

        for num in range(0, 10):
            sizeXmg, sizeYimg = 80, 80

            img = pygame.image.load(f'boy/Dead__00{num}.png')
            img = pygame.transform.scale(img, (sizeXmg, sizeYimg))
            self.img_dead.append(img)

            img = pygame.image.load(f'boy/Idle__00{num}.png')
            img = pygame.transform.scale(img, (sizeXmg, sizeYimg))
            self.img_stay.append(img)

            img = pygame.image.load(f'boy/Jump__00{num}.png')
            img = pygame.transform.scale(img, (sizeXmg, sizeYimg))
            self.img_jump.append(img)

            img = pygame.image.load(f'boy/Run__00{num}.png')
            img = pygame.transform.scale(img, (sizeXmg, sizeYimg))
            self.img_run.append(img)

            img = pygame.image.load(f'boy/Slide__00{num}.png')
            img = pygame.transform.scale(img, (sizeXmg, sizeYimg))
            self.img_slide.append(img)
        self.index = 0
        self.image = self.img_stay[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = screenH/2-groundH/2-self.rect.height
        self.vel_y = 0
        self.state = "stay"  # "stay" "run" "slide" "dead" "jump"
        self.side = 1  # prawa w prawo idze -1 dół w lewo
        self.index_jump = 0

        self.counter = 0

    def update(self):
        dx = 0
        dy = 0

        walk_cooldown = 3

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not self.state == "jump":
            if self.side == 1:
                self.vel_y = -15
                self.state = "jump"
                self.index = 0
            if self.side == -1:######################################################################
                self.vel_y = 15
                self.state = "jump"
                self.index = 0
        #-----------------LEFT DOWN -----------------------
        if key[pygame.K_LEFT] and not self.state == "jump":
            self.rect.y = screenH /2 +(groundH / 2)
            dx -= 5
            self.side = -1

            if not self.state == "run":
                self.index = 0
                self.state = "run"
        if key[pygame.K_LEFT] and self.state == "jump" and self.side == -1:
            dx -= 5
        #--------------RIGHT UP ---------------------------
        if key[pygame.K_RIGHT] and not self.state == "jump":
            self.rect.y = screenH / 2 - groundH / 2 - self.rect.height
            self.side = 1
            self.vel_y = 10
            dx += 5
            if not self.state == "run":
                self.index = 0
                self.state = "run"
        if key[pygame.K_RIGHT] and self.state == "jump" and self.side == 1:
            dx += 5
        ##-----------------------SLIDE------------------------------------------------
        if key[pygame.K_DOWN] and (self.state == "run" or self.state == "stay") and self.side == 1:
            self.side = 1
            if not self.state == "slide":
                self.index = 0
            self.state = "slide"
        if key[pygame.K_DOWN] and (self.state == "run" or self.state == "stay") and self.side == -1:
            self.side = -1
            if not self.state == "slide":
                self.index = 0
            self.state = "slide"
        #----------STAY------------------------------
        if self.state == "run":
            if key[pygame.K_RIGHT] == False:
                if not key[pygame.K_LEFT]:
                    self.state = "stay"
                    self.index = 0

        # animation
        self.counter +=1
        if self.counter > walk_cooldown: #can do slow motion here
            self.counter = 0
            self.index += 1

        if self.state == "jump":
            self.index_jump += 1
            self.index = math.floor(self.index_jump / 3)
            if self.index >= len(self.img_jump):
                self.index = 0
                self.state = "stay"
                self.index_jump = 0

        if self.state == "slide":
            if self.side == 1:
                dx += 1
            elif self.side == -1:
                dx -= 1
            if self.index == len(self.img_slide):
                self.state = "stay"

        if self.index >= len(self.img_stay):  #####can change to couple
            self.index = 0

        if self.state == "stay" and self.side == 1:
            self.image = self.img_stay[self.index]
        elif self.state == "stay" and self.side == -1:
            self.rect.y = screenH / 2 + groundH/2
            self.image = pygame.transform.flip(self.img_stay[self.index], True, True)
        elif self.state == "run" and self.side == 1:
            self.image = self.img_run[self.index]
            self.rect.y=screenH/2-groundH/2-self.rect.height
        elif self.state == "run" and self.side == -1:
            self.image = pygame.transform.flip(self.img_run[self.index], True, True)
            self.rect.y=screenH/2+groundH/2
        elif self.state == "jump" and self.side == 1:
            self.image = self.img_jump[self.index]
        elif self.state == "jump" and self.side == -1:
            self.image = pygame.transform.flip(self.img_jump[self.index], True, True)
        elif self.state == "slide" and self.side == 1:
            self.image = self.img_slide[self.index]
        elif self.state == "slide" and self.side == -1:
            self.image = pygame.transform.flip(self.img_slide[self.index], True, True)
        elif self.state == "dead":
            self.image = self.img_dead[self.index]

        ## add gravity
        '''
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        '''
        if self.side == 1:
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
            
        elif self.side == -1:
            self.vel_y -= 1
            if self.vel_y < -10:
                self.vel_y = -10
            dy += self.vel_y
        #'''
        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy


        # grawity so he must stay on ground
        if self.side == 1:
            if self.rect.top > screenH/2-groundH/2-self.rect.height:
                self.rect.top = screenH/2-groundH/2-self.rect.height
                dy = 0
        elif self.side == -1:
            if self.rect.top < screenH/2+groundH/2:
                self.rect.top = screenH/2+groundH/2
                dy = 0

        from main import screen
        screen.blit(self.image, self.rect)
