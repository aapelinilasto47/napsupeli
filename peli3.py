from os import path
import pygame
from pygame.locals import *
import random
import json


pygame.init()

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(8)

clock = pygame.time.Clock()
fps = 60
level = 1



start_time = pygame.time.get_ticks()

screen_width = 1500
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Napsu Peli")

# Load images


tausta = pygame.image.load("tausta.png")
restart_image = pygame.image.load("restart1.png")
background_image = pygame.image.load("mainmenu.jpg")
maali_image = pygame.image.load("apenaama.png")


damagenoise = pygame.mixer.Sound("damage jani.mp3")
damagenoise.set_volume(0.5)

napsunoise = pygame.mixer.Sound("napsuu.wav")
napsunoise.set_volume(0.5)

pygame.mixer.music.load("tausta.mp3")
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(-1)




tile_size = 25
game_over = 0

napsu_score = 0

mainmenu = True


def draw_text():
    global napsu_score, elapsed_time, level

    block = pygame.Surface((500, 50))
    block.fill((5, 5, 5))
    screen.blit(block, (0, 0))

    score_text = pygame.font.Font(None, 36).render("Napsut: " + str(napsu_score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    time_text = pygame.font.Font(None, 36).render("Aika: " + str(elapsed_time) + "s", True, (255, 255, 255))
    screen.blit(time_text, (150, 10))

    level_text = pygame.font.Font(None, 36).render("Taso: " + str(level), True, (255, 255, 255))
    screen.blit(level_text, (300, 10))

def draw_grid():
    for x in range(0, screen_width, tile_size):
        for y in range(0, screen_height, tile_size):
            rect = pygame.Rect(x, y, tile_size, tile_size)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)


def levelload():
    global world_data
    if path.exists(f'level{level}_data.json'):
        with open(f'level{level}_data.json', 'r') as level_file:
            world_json = json.load(level_file)
            world_data = world_json["worldtiles"]

def enemyreset():
    global enemy_pos, statenemy_pos, collectible_pos, ladder_pos, goal_pos, vert_enemy_pos, double_collectible_pos
    enemy_group.empty()
    enemy_pos = [enemy_group.add(Enemy(x * tile_size, y * tile_size)) for y, row in enumerate(world_data) for x, tile in enumerate(row) if tile == 2]
    vert_enemy_group.empty()
    vert_enemy_pos = [vert_enemy_group.add(VertEnemy(x * tile_size, y * tile_size)) for y, row in enumerate(world_data) for x, tile in enumerate(row) if tile == 7]
    statenemy_group.empty()
    statenemy_pos = [statenemy_group.add(StatEnemy(x * tile_size, y * tile_size)) for y, row in enumerate(world_data) for x, tile in enumerate(row) if tile == 3]
    collectible_group.empty()
    collectible_pos = [collectible_group.add(Collectible(x * tile_size, y * tile_size)) for y, row in enumerate(world_data) for x, tile in enumerate(row) if tile == 4]
    double_collectible_group.empty()
    double_collectible_pos = [double_collectible_group.add(DoubleCollectible(x * tile_size, y * tile_size)) for y, row in enumerate(world_data) for x, tile in enumerate(row) if tile == 9]
    goal_group.empty()
    goal_pos = [goal_group.add(Goal(x * tile_size, y * tile_size)) for y, row in enumerate(world_data) for x, tile in enumerate(row) if tile == 5]
    ladder_group.empty()
    ladder_pos = [ladder_group.add(Ladder(x * tile_size, y * tile_size)) for y, row in enumerate(world_data) for x, tile in enumerate(row) if tile == 6]

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False


    def draw(self):

        action = False

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            # Change the button image or perform an action
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                
                action = True
                self.clicked = True

                
            elif not pygame.mouse.get_pressed()[0]:
                self.clicked = False

        screen.blit(self.image, self.rect)

        return action

class Player():
    def __init__(self, x, y):
        self.reset(x, y)


    def update(self, game_over):


        dx = 0
        dy = 0
        walk_cooldown = 10
        


        global napsu_score, collectible_pos, enemy_pos, statenemy_pos, start_time, elapsed_time, level, world

        if game_over == 0:       
            #get keypresses

            
            world.draw()
            enemy_group.draw(screen)
            vert_enemy_group.draw(screen)
            collectible_group.draw(screen)
            double_collectible_group.draw(screen)
            statenemy_group.draw(screen)

            draw_text()

            key = pygame.key.get_pressed()



            

                
            self.rect.width = 22
            self.rect.height = 45
            self.width = self.rect.width
            self.height = self.rect.height

            if self.direction < 0:
                self.image = self.images_left[self.index]
            elif self.direction > 0:
                self.image = self.images_right[self.index]

            if (key[pygame.K_LEFT] or key[pygame.K_a]) and not key[pygame.K_LCTRL]:
                dx = -2
                self.counter += 1
                self.direction = -1


            if (key[pygame.K_RIGHT] or key[pygame.K_d]) and not key[pygame.K_LCTRL]:
                dx = 2
                self.counter += 1
                self.direction = 1


            if not key[pygame.K_RIGHT] and not key[pygame.K_LEFT] and not key[pygame.K_a] and not key[pygame.K_d]:
                self.counter = 0
                self.index = 0
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                
                elif self.direction == 1:
                    self.image = self.images_right[self.index]

            if key[pygame.K_SPACE] and self.jumped == False:
                self.vel_y = -12
                self.jumped = True


            

            #animation
            
            if self.counter >= walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                    
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                
                elif self.direction == 1:
                    self.image = self.images_right[self.index]

            #gravity


            self.vel_y += 1  # gravity effect
            if self.vel_y > 6:
                self.vel_y = 6
            dy += self.vel_y
            
            #collisions

            for tile in world.tile_list:

                #collision on x
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                    self.rect.x += dx
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.jumped = False

            #enemy collision
            if pygame.sprite.spritecollide(self, enemy_group, False) and napsu_score == 0:
                game_over = -1

                damagenoise.play()

                self.rect.y = self.rect.y + 25
                if self.rect.y > screen_height:
                    self.rect.y = screen_height

            elif pygame.sprite.spritecollide(self, enemy_group, True) and napsu_score > 0:
                napsu_score -= 1


            elif pygame.sprite.spritecollide(self, vert_enemy_group, False) and napsu_score == 0:
                game_over = -1

                damagenoise.play()
                self.rect.y = self.rect.y + 25
                if self.rect.y > screen_height:
                    self.rect.y = screen_height

            elif pygame.sprite.spritecollide(self, vert_enemy_group, True) and napsu_score > 0:
                napsu_score -= 1

            elif pygame.sprite.spritecollide(self, statenemy_group, False) and napsu_score == 0:
                game_over = -1

                damagenoise.play()
                

                self.rect.y = self.rect.y + 25
                if self.rect.y > screen_height:
                    self.rect.y = screen_height

            elif pygame.sprite.spritecollide(self, statenemy_group, True):
                napsu_score -= 1

                

            #collectibles collision

            elif pygame.sprite.spritecollide(self, collectible_group, True):
                napsu_score += 1

                napsunoise.play()

            elif pygame.sprite.spritecollide(self, double_collectible_group, True):
                napsu_score += 2

                napsunoise.play()

            elif pygame.sprite.spritecollide(self, goal_group, False):
                game_over = 1

            #ladder collision
            if pygame.sprite.spritecollide(self, ladder_group, False):
                
                if key[pygame.K_UP] or key[pygame.K_w]:
                    self.rect.y -= 10
                

            #player out of screen
            if self.rect.x < 0 or self.rect.x > screen_width:
                self.rect.x = 0
            if self.rect.y < 0 or self.rect.y > screen_height:
                self.rect.y = 0

            #update player position
            self.rect.x += dx
            self.rect.y += dy

        #check for death
        elif game_over == -1:


            


            self.image = self.dead_image

            block = pygame.Surface((700, 200))
            block.fill((5, 5, 5))
            screen.blit(block, (400, 350))

            deadtext = pygame.font.Font(None, 74)
            dead_surface = deadtext.render("Et ole enää napsuissa!", True, (255, 0, 0))
            screen.blit(dead_surface, (screen_width // 2 - dead_surface.get_width() // 2, screen_height // 2 - dead_surface.get_height() // 2))

            replay_text = pygame.font.Font(None, 36)
            replay_surface = replay_text.render("Paina Enteriä pelataksesi uudelleen", True, (255, 255, 255))
            screen.blit(replay_surface, (screen_width // 2 - replay_surface.get_width() // 2, screen_height // 2 + 50))

            end_timetext = pygame.font.Font(None, 36)
            end_timesurface = end_timetext.render(f"Aika: {elapsed_time}s", True, (255, 255, 255))
            screen.blit(end_timesurface, (screen_width // 2 - end_timesurface.get_width() // 2, screen_height // 2 + 100))

            start_time = pygame.time.get_ticks()

            key = pygame.key.get_pressed()
            if key[pygame.K_RETURN]:
                
                game_over = 0
                napsu_score = 0
                self.rect.x = 50
                self.rect.y = 800
                level = 1

                enemyreset()
                levelload()
                world = World(world_data)

        #draw player
        screen.blit(self.image, self.rect)

        return game_over
        

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []

        self.index = 0
        self.counter = 0

        for num in range(4, 7):
            img_right = pygame.image.load(f"askel{num}.png")
            img_right = pygame.transform.scale(img_right, (22, 45))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.dead_image = pygame.image.load("dead.png")
        self.dead_image = pygame.transform.scale(self.dead_image, (tile_size *2, tile_size))

        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0






class World():
    def __init__(self, data):
        
        global tile_size
        self.tile_list = []

        
        # Load tile image
        este = pygame.image.load("este.png")
        maa = pygame.image.load("asfaltti.png")



        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    este = pygame.transform.scale(este, (tile_size, tile_size))
                    este_rect = este.get_rect()
                    este_rect.x = col_count * tile_size
                    este_rect.y = row_count * tile_size
                    tile = (este, este_rect)
                    self.tile_list.append(tile)

                if tile == 2:
                    enemy = Enemy(col_count * tile_size, row_count * tile_size)
                    enemy_group.add(enemy)

                if tile == 3:
                    stat_enemy = StatEnemy(col_count * tile_size, row_count * tile_size)
                    statenemy_group.add(stat_enemy)

                if tile == 4:
                    collectible = Collectible(col_count * tile_size, row_count * tile_size)
                    collectible_group.add(collectible)

                if tile == 5:
                    goal = Goal(col_count * tile_size, row_count * tile_size)
                    goal_group.add(goal)

                if tile == 8:
                    maa = pygame.transform.scale(maa, (tile_size, tile_size))
                    este_rect = maa.get_rect()
                    este_rect.x = col_count * tile_size
                    este_rect.y = row_count * tile_size
                    tile = (maa, este_rect)
                    self.tile_list.append(tile)

                col_count += 1
            row_count += 1

    def draw(self):

        
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("vesipullo.png")
        self.image = pygame.transform.scale(self.image, (15, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1  # 1 for right, -1 for left
        self.move_counter = 0

    def update(self):
        # Enemy movement logic can be added here
        self.rect.x += self.move_direction  # Move enemy horizontally
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1  # Change direction after 100 frames
            self.move_counter *= -1

class VertEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("vesipullo.png")
        self.image = pygame.transform.scale(self.image, (15, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1  # 1 for down, -1 for up
        self.move_counter = 0

    def update(self):
        # Enemy movement logic can be added here
        self.rect.y += self.move_direction  # Move enemy vertically
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1  # Change direction after 100 frames
            self.move_counter *= -1

class StatEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bigmac.png")
        self.image = pygame.transform.scale(self.image, (22, 22))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    
        # Static enemy logic can be added here

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("napsu.png")
        self.image = pygame.transform.scale(self.image, (18, 18))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Collectible logic can be added here

class DoubleCollectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("tuplanapsu.png")
        self.image = pygame.transform.scale(self.image, (30, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 20

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = maali_image
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Ladder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ladder.png")
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

player = Player(50, 800)

enemy_group = pygame.sprite.Group()

vert_enemy_group = pygame.sprite.Group()

statenemy_group = pygame.sprite.Group()

collectible_group = pygame.sprite.Group()

double_collectible_group = pygame.sprite.Group()

goal_group = pygame.sprite.Group()

ladder_group = pygame.sprite.Group()

if path.exists(f'level{level}_data.json'):
    with open(f'level{level}_data.json', 'r') as level_file:
        world_json = json.load(level_file)
        world_data = world_json["worldtiles"]   # <- Ota itse lista ulos
        print("Level loaded:", len(world_data), "riviä")

if level == 1:
    world = World(world_data)

enemy_pos = [enemy_group.add(Enemy(x * tile_size, y * tile_size)) for y, row in enumerate(world_data) for x, tile in enumerate(row) if tile == 2]

vert_enemy_pos = [vert_enemy_group.add(VertEnemy(x * tile_size, y * tile_size)) for y, row in enumerate(world_data) for x, tile in enumerate(row) if tile == 7]

statenemy_pos = [statenemy_group.add(StatEnemy(x * tile_size, y * tile_size)) for y, row in enumerate(world_data) for x, tile in enumerate(row) if tile == 3]

collectible_pos = [collectible_group.add(Collectible(x * tile_size, y * tile_size)) for y, row in enumerate(world_data) for x, tile in enumerate(row) if tile == 4]

double_collectible_pos = [double_collectible_group.add(DoubleCollectible(x * tile_size, y * tile_size)) for y, row in enumerate(world_data) for x, tile in enumerate(row) if tile == 9]

goal_pos = [goal_group.add(Goal(x * tile_size, y * tile_size)) for y, row in enumerate(world_data) for x, tile in enumerate(row) if tile == 5]

ladder_pos = [ladder_group.add(Ladder(x * tile_size, y * tile_size)) for y, row in enumerate(world_data) for x, tile in enumerate(row) if tile == 6]

#load level data and create world







restart_button = Button(650, 600, pygame.image.load("restart1.png"))
restart_button.image = pygame.transform.scale(restart_button.image, (200, 100))

main_menu_background = pygame.transform.scale(background_image, (screen_width, screen_height))



run = True

while run:


    if mainmenu:
        # Draw main menu elements
        screen.blit(main_menu_background, (0, 0))
        title_font = pygame.font.Font(None, 100)
        title_surface = title_font.render("Napsu peli", True, (255, 255, 255))
        screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, 100))

        start_button = Button(screen_width // 2 - 200, 600, pygame.image.load("startnappi.png"))
        start_button.image = pygame.transform.scale(start_button.image, (400, 100))
        if start_button.draw():
            mainmenu = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            mainmenu = False


    else:

        clock.tick(fps)
        screen.blit(tausta, (0, 0))

        

        world.draw()

        enemy_group.update()
        enemy_group.draw(screen)

        vert_enemy_group.update()
        vert_enemy_group.draw(screen)

        statenemy_group.update()
        statenemy_group.draw(screen)

        collectible_group.update()
        collectible_group.draw(screen)

        double_collectible_group.update()
        double_collectible_group.draw(screen)

        goal_group.update()
        goal_group.draw(screen)

        ladder_group.update()
        ladder_group.draw(screen)

        if game_over == 0:

            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            

        
            
                


        if game_over == 1:

            block = pygame.Surface((500, 300))
            block.fill((5, 5, 5))
            screen.blit(block, (500, 350))

            win_text = pygame.font.Font(None, 74)
            win_surface = win_text.render("Voitit!", True, (255, 255, 255))
            screen.blit(win_surface, (screen_width // 2 - win_surface.get_width() // 2, screen_height // 2 - win_surface.get_height() // 2))

            win_subtext = pygame.font.Font(None, 36)
            win_subsurface = win_subtext.render("Selvisit Apen luo napsuissa.", True, (255, 255, 255))
            screen.blit(win_subsurface, (screen_width // 2 - win_subsurface.get_width() // 2, screen_height // 2 - win_subsurface.get_height() // 2 + 50))

            timer_text = pygame.font.Font(None, 36)
            end_timer_surface = timer_text.render(f"Aika: {elapsed_time}s", True, (255, 255, 255))
            screen.blit(end_timer_surface, (screen_width // 2 - end_timer_surface.get_width() // 2, screen_height // 2 - end_timer_surface.get_height() // 2 + 100))

            nextlevel_text = pygame.font.Font(None, 36)
            nextlevel_surface = nextlevel_text.render("Paina Enteriä jatkaaksesi seuraavalle tasolle, tai paina ESC jos haluat poistua", True, (255, 255, 255))
            screen.blit(nextlevel_surface, (screen_width // 2 - nextlevel_surface.get_width() // 2, screen_height // 2 - nextlevel_surface.get_height() // 2 + 150))

            



            key = pygame.key.get_pressed()
            if key[pygame.K_RETURN]:
                player.reset(50, 800)
                game_over = 0
                
                napsu_score = 0
                level += 1
                levelload()
                enemyreset()

                world = World(world_data)

            if key[pygame.K_ESCAPE]:
                run = False



        game_over = player.update(game_over)



        if game_over == -1:
            level = 1
            levelload()
            
            

            
            if restart_button.draw():
                
                game_over = 0
                enemyreset()
                

                start_time = pygame.time.get_ticks()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.display.update()

    

pygame.quit()