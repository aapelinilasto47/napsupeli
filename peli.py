import pygame
import sys
import random
import time


pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Peli")

kuva = pygame.image.load("monsu2.png")
kuva = pygame.transform.scale(kuva, (115/4, 375/4))

x = 360
y = 400
x_speed = 0
y_speed = 0


esteet = []

for i in range(3):
    este = pygame.Rect(random.randint(0, 800), random.randint(0, 600), 10, 10)
    esteet.append(este)

piste = pygame.Rect(random.randint(0, 800), random.randint(0, 600), 10, 10)

clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()


running = True
run = False
paused = False
game_over = False

kerrat = 0
points = 0

# colors

black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)
dark_gray = (50, 50, 50)
light_gray = (220, 220, 220)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
monster_color = (197, 225, 122)


def player(x,y):
    screen.blit(kuva, (x, y))







def pause():
    global run, running, paused
    screen.fill((dark_gray))
    screen.blit(pygame.font.SysFont("Arial", 36).render("Peli Paussattu", True, (white)), (300, 250))
    screen.blit(pygame.font.SysFont("Arial", 24).render("Paina Enter jatkaaksesi tai Esc lopettaaksesi", True, (white)), (200, 300))
    pygame.display.flip()
    clock.tick(60)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                run = True
                paused = False
            if event.key == pygame.K_ESCAPE:
                running = False
                paused = False


def game_over_screen():
    global run, running, game_over, paused, points
    screen.fill(dark_gray)
    screen.blit(pygame.font.SysFont("Arial", 36).render("Peli Ohi", True, (red)), (300, 250))
    screen.blit(pygame.font.SysFont("Arial", 24).render(f"Pisteet: {points}", True, (white)), (300, 300))
    screen.blit(pygame.font.SysFont("Arial", 24).render(f"Aika: {elapsed_time:.2f} s", True, (white)), (300, 350))
    screen.blit(pygame.font.SysFont("Arial", 24).render(f"Pisteet per sekunti: {points / elapsed_time:.2f}" if elapsed_time > 0 else "Pisteet per sekunti: 0.00", True, (white)), (200, 400))
    pygame.display.flip()
    clock.tick(60)
    


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                run = False
                paused = False
                game_over = False
            if event.key == pygame.K_ESCAPE:
                running = False
                game_over = False

def boost():
    global x_speed, y_speed
    x_speed *= 2
    y_speed *= 2


# Main game loop


while running:

    if not paused and not run and not game_over:
        points = 0
        screen.fill(dark_gray)
        screen.blit(pygame.font.SysFont("Arial", 36).render("Paina Enter aloittaaksesi", True, (white)), (300, 250))
        screen.blit(pygame.font.SysFont("Arial", 24).render("Paina Esc lopettaaksesi", True, (red)), (300, 300))
        pygame.display.flip()
        clock.tick(60)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = True
                if event.key == pygame.K_ESCAPE:
                    running = False

        

    while run:
        screen.fill(dark_gray)
        screen.blit(pygame.font.SysFont("Arial", 24).render(f"Pisteet: {points}", True, (white)), (10, 10))
        player(x, y)
        pygame.draw.rect(screen, monster_color, piste)
        for este in esteet:
            pygame.draw.rect(screen, light_gray, este)
        pygame.display.flip()
        clock.tick(60)
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # seconds
        screen.blit(pygame.font.SysFont("Arial", 24).render(f"Aika: {elapsed_time:.2f} s", True, (white)), (10, 40))

        if este.colliderect(kuva.get_rect(topleft=(x, y))):
            game_over = True
            run = False
            paused = False
            x = 360
            y = 400
            x_speed = 0
            y_speed = 0

        if piste.colliderect(kuva.get_rect(topleft=(x, y))):
            points += 1
            piste.x = random.randint(0, 800)
            piste.y = random.randint(0, 600)

            este = pygame.Rect(random.randint(0, 800), random.randint(0, 600), 10, 10)
            esteet.append(este)

            for este in esteet:
                este.x = random.randint(0, 800)
                este.y = random.randint(0, 600)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_speed = -2
                if event.key == pygame.K_RIGHT:
                    x_speed = 2
                if event.key == pygame.K_UP:
                    y_speed = -2
                if event.key == pygame.K_DOWN:
                    y_speed = 2
                if event.key == pygame.K_LSHIFT:
                    boost()

                if event.key == pygame.K_a:
                    x_speed = -2
                if event.key == pygame.K_d:
                    x_speed = 2
                if event.key == pygame.K_w:
                    y_speed = -2
                if event.key == pygame.K_s:
                    y_speed = 2

                if event.key == pygame.K_ESCAPE:
                    run = False
                    paused = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_speed = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_speed = 0

                if event.key == pygame.K_a or event.key == pygame.K_d:
                    x_speed = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    y_speed = 0

                if event.key == pygame.K_LSHIFT:
                    x_speed /= 2
                    y_speed /= 2
                    

        x += x_speed
        y += y_speed


        if x < 0:
            x = 0
        if x > 771:
            x = 771
        if y < 0:
            y = 0
        if y > 508:
            y = 508

    if paused:
        pause()
        pygame.display.flip()
        clock.tick(60)

    kerrat += 1

    if game_over:
        game_over_screen()
        clock.tick(60)

pygame.quit()