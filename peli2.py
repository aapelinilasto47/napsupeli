import pygame
import sys
import random

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Napsu Peli")



jani = pygame.transform.scale(pygame.image.load("jamppa.png"), (200, 200))

clock = pygame.time.Clock()
fps = 60


tile_size = 50


tausta = pygame.image.load("tausta.png")


def draw_grid():
    for line in range(0, screen_height, tile_size):
        pygame.draw.line(screen, (255, 255, 255), (0, line), (screen_width, line))
    for line in range(0, screen_width, tile_size):
        pygame.draw.line(screen, (255, 255, 255), (line, 0), (line, screen_height))


def mainmenu():
    global Mainmenu, run
    screen.blit(tausta, (0, 0))


    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                Mainmenu = False
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.QUIT:
            run = False



class Player():
    def __init__(self, x, y):

        hahmo = pygame.image.load("hahmo2.png")
        hahmo = pygame.transform.scale(hahmo, (50, 100))

        self.rect = self.get_rect(topleft=(x, y))
        self.rect.x = x
        self.rect.y = y

    def update(self):


        walkLeft = [pygame.transform.scale(pygame.image.load("askel1.png"), (50, 100)),
             pygame.transform.scale(pygame.image.load("askel2.png"), (50, 100)),
             pygame.transform.scale(pygame.image.load("askel3.png"), (50, 100))]

        walkRight = [pygame.transform.scale(pygame.image.load("askel4.png"), (50, 100)),
            pygame.transform.scale(pygame.image.load("askel5.png"), (50, 100)),
            pygame.transform.scale(pygame.image.load("askel6.png"), (50, 100))]
        
        hahmo_x = 0
        hahmo_y = 450

        x_liike = 0
        y_liike = 0

        neg = 0


        jumpcount = 10

        walkcount = 0


        dx = 0
        dy = 0




        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx = -3
            screen.blit(walkLeft[walkcount // 3], (hahmo_x, hahmo_y))
            hahmo_rect = self.get_rect(topleft=(hahmo_x, hahmo_y))
            pygame.draw.rect(screen, (255, 0, 0), hahmo_rect, 2)

            walkcount += 1
            if walkcount >= 9:
                walkcount = 0
        if key[pygame.K_RIGHT]:
            dx = 3
            screen.blit(walkRight[walkcount // 3], (hahmo_x, hahmo_y))
            hahmo_rect = sel.get_rect(topleft=(hahmo_x, hahmo_y))
            pygame.draw.rect(screen, (255, 0, 0), hahmo_rect, 2)

            walkcount += 1
            if walkcount >= 9:
                walkcount = 0

        if key[pygame.K_SPACE]:
            if jumpcount >= -10:
                neg = 1
                if jumpcount < 0:
                    neg = -1
                y_liike = (jumpcount ** 2) * 0.1 * neg
                hahmo_y -= y_liike
                jumpcount -= 0.5
                    
                
            else:
                jumpcount = 10





        self.rect.x += dx
        self.rect.y += dy
        screen.blit(self, (self.rect.x, self.rect.y))
        hahmo_rect = self.get_rect(topleft=(self.rect.x, self.rect.y))
        pygame.draw.rect(screen, (255, 0, 0), hahmo_rect, 2)


    
    



        


class World:
    def __init__(self, data):

        

        self.tile_list = []
        
        este = pygame.image.load("este.png")

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(este, (tile_size, tile_size))
                    palikka = img.get_rect()
                    palikka.x = col_count * tile_size
                    palikka.y = row_count * tile_size
                    tile = (img, palikka)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

        

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


world = World(world_data)








run = True
Mainmenu = True


while run:


    if Mainmenu:
        mainmenu()
        pygame.display.flip()

    else:
        clock.tick(fps)
        screen.blit(tausta, (0, 0))
        world.draw()
        draw_grid()

        player = Player(100, 450)

        player.update()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        

        pygame.display.flip()
    



pygame.quit()
