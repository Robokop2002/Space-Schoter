import pygame.event
from pygame import *
import time as ti
import random

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire = mixer.Sound('fire.ogg')

window = display.set_mode((1400, 800))
display.set_caption('schoter')
clock = time.Clock()
FPS = 60
font.init()
font1 = font.Font('Pacifico-Regular.ttf', 125)
font2 = font.Font('Pacifico-Regular.ttf', 40)
font3 = font.Font('Pacifico-Regular.ttf', 70)

Speed = 10
speed_enemy = (1, 2)
col_enemy = 6

background = transform.scale(image.load('galaxy.jpg'), (1400, 800))

sbito = 0
propustino = 0
schisni = 3

class Game_Sprite(sprite.Sprite):
    def __init__(self, image_sprite, x, y, speed, width, height):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(image_sprite), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Game_Sprite):
    max_patron_col = 5
    reload_gun = False
    bullets_col = 0
    a = ti.time()
    b = 0
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_a]:
            self.rect.x -= self.speed
        if keys_pressed[K_d]:
            self.rect.x += self.speed

        if keys_pressed[K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT]:
            self.rect.x += self.speed

        if self.rect.x >= 1300:
            self.rect.x = 1299
        if self.rect.x <= 0:
            self.rect.x = 1

        if self.rect.y >= 700:
            self.rect.y = 699
        if self.rect.y <= 0:
            self.rect.y = 1

    def fire(self):
        if self.a >= self.b:
            if self.bullets_col >= self.max_patron_col:
                self.bullets_col = 0
                self.a = ti.time()
                self.b = self.a + 3
                self.reload_gun = True
            else:
                self.bullets_col += 1
                bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 20, 50)
                bullets.add(bullet)
                fire.play()
                self.reload_gun = False
        else:
            self.reload_gun = True

class Enemy(Game_Sprite):
    def __init__(self, image_sprite, speed, width, height):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(image_sprite), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1300)
        self.rect.y = 50
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

        if self.rect.y >= 700:
            global propustino
            propustino += 1
            self.tp()
    def tp(self):
        self.rect.x = random.randint(0, 1400)
        self.rect.y = -50

class Meteor(Game_Sprite):
    def __init__(self, image_sprite, width, height):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(image_sprite), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1300)
        self.rect.y = 50
        self.speed = 4

    def update(self):
        self.rect.y += self.speed

        if self.rect.y >= 700:
            self.tp()
    def tp(self):
        self.rect.x = random.randint(0, 1400)
        self.rect.y = -50

class Bullet(Game_Sprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y <= 0:
            self.kill()

player = Player('rocket.png', 700, 650, Speed, 100, 150)
meteor = Meteor('asteroid.png', 100, 100)

win = font1.render('Mission Complete', True, (0, 0, 0))
game_over = font1.render('Mission failed', True, (40, 0, 0))
reload = font2.render('gun reloading', True, (255, 0, 0))
game = True
finisch = False

monsters = sprite.Group()
bullets = sprite.Group()

for i in range(1, 7):
    monsters.add(Enemy('ufo.png', random.randint(speed_enemy[0], speed_enemy[1]), 100, 50))

while game:
    keys_pressed = key.get_pressed()
    for i in event.get():
        if i.type == QUIT:
            game = False

        if i.type == MOUSEBUTTONDOWN:
            player.fire()

    if finisch != True:
        player.a = ti.time()
        window.blit(background, (0, 0))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        meteor.reset()
        meteor.update()

        bullets.draw(window)
        bullets.update()

        if player.a >= player.b:
            player.reload_gun = False
        else:
            player.reload_gun = True

        if player.reload_gun == True:
            window.blit(reload, (600, 720))

        if sprite.spritecollide(player, monsters, True):
            schisni -= 1
            if schisni <= 0:
                finisch = True
                window.blit(game_over, (300, 330))

        if propustino >= 3:
            schisni -= 1
            propustino = 0
            if schisni <= 0:
                finisch = True
                window.blit(game_over, (300, 330))

        if sprite.collide_rect(player, meteor):
            schisni -= 1
            if schisni <= 0:
                finisch = True
                window.blit(game_over, (300, 330))
            meteor.tp()

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for x in sprites_list:
            monsters.add(Enemy('ufo.png', random.randint(speed_enemy[0], speed_enemy[1]), 100, 50))
            sbito += 1
            if sbito >= 10:
                finisch = True
                window.blit(win, (280, 330))

        sbito_gui = font2.render(f'сбито  {sbito}', True, (111, 255, 0))
        propustino_gui = font2.render(f'пропущено  {propustino}', True, (111, 255, 0))
        if schisni == 3:
            schisn_gui = font1.render(f'{schisni}', True, (28, 255, 8))
        elif schisni == 2:
            schisn_gui = font1.render(f'{schisni}', True, (251, 255, 0))
        elif schisni == 1:
            schisn_gui = font1.render(f'{schisni}', True, (255, 0, 0))
        elif schisni == 0:
            schisn_gui = font1.render(f'{schisni}', True, (255, 0, 0))
        window.blit(sbito_gui, (0, 0))
        window.blit(propustino_gui, (0, 30))
        window.blit(schisn_gui, (700, 30))

    else:
        ti.sleep(5)
        for i in bullets:
            i.kill()

        for i in monsters:
            i.kill()

        for i in range(1, 7):
            monsters.add(Enemy('ufo.png', random.randint(speed_enemy[0], speed_enemy[1]), 100, 50))

        player.rect.x = 700

        sbito = 0
        propustino = 0

        finisch = False

    display.update()
    clock.tick(FPS)

