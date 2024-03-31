import pygame, time
import random
from pygame.locals import *
# init
pygame.init()

# initialize constants
SIZE = WIDTH, HEIGHT = 400, 600
FPS = 60
SPEED = 5
SPEED_ENEMY = 5
SCORE = 0
SCORE_COINS = 0

# basic colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0, 255, 0)

# init fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 18)
game_over = font.render("Game Over", True, BLACK)

# init background image
background = pygame.image.load("AnimatedStreet.png")

# set screen size and set caption
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Racer")

done = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

    # enemy behaviour
    def move(self):
        self.rect.move_ip(0, SPEED_ENEMY)
        if self.rect.bottom > 600:
            global SCORE
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    # player controls
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-SPEED,0)
        if self.rect.right < WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(SPEED,0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, WIDTH - 30), 0)

    # randomly appearing coin behaviour
    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40), 0)

P1 = Player()
E1 = Enemy()
C1 = Coin()

# sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(E1)
all_sprites.add(P1)
all_sprites.add(C1)

# add new user event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while not done:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

        # increase speed of enemies over time
        if event.type == INC_SPEED:
            SPEED_ENEMY += 0.25

    # show score and load background
    screen.blit(background, (0,0))
    scores = font_small.render("Score:"+str(SCORE), 1, BLACK)
    scores_coins = font_small.render("Coins:"+str(SCORE_COINS), 1, GREEN)
    screen.blit(scores, (10,10))
    screen.blit(scores_coins, (315, 10))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    # if player collides with enemy, show game over and exit
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("crash.wav")
        time.sleep(1)

        screen.fill(RED)
        screen.blit(game_over, (20, 250))
        screen.blit(scores, (165, 330))
        screen.blit(scores_coins, (165, 350))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(1)
        done = True

    # if player collides with coins, increase coin score
    if pygame.sprite.spritecollideany(P1, coins):
        SCORE_COINS += 1
        C1.rect.top = 0
        C1.rect.center = (random.randint(40, WIDTH - 40), 0)

    # to make sure coins are not in enemy hitbox
    if pygame.sprite.spritecollideany(C1, enemies):
        C1.rect.top = 0
        C1.rect.center = (random.randint(40, WIDTH - 40), 0)
        time.sleep(0.5)

    pygame.display.update()
    clock.tick(FPS)
