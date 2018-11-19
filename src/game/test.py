import pygame
import random
import os
from settings import *
from sprite import *


class Game:
    def __init__(self):

        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):

        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self. player)
        base = Base(0, HEIGHT - 30, WIDTH , 30)
        self.all_sprites.add(base)
        self.platforms.add(base)
        plat1 = Base(60, 420, 200, 50)
        self.all_sprites.add(plat1)
        self.platforms.add(plat1)
        plat2 = Base(435, 420, 200, 50)
        self.all_sprites.add(plat2)
        self.platforms.add(plat2)
        plat3 = Base(250, 200, 200, 50)
        self.all_sprites.add(plat3)
        self.platforms.add(plat3)
        self.run() 

    def run(self):
        
        self.playing = True

        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if keys[pygame.K_UP]:
                self.player.jump()

    def update(self):

        self.all_sprites.update()

        if self.player.vel.y > 0:
            collision = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if collision:
                self.player.pos.y = collision[0].rect.top + 1
                self.player.vel.y = 0

        # if self.player.rect.top < HEIGHT / 28:
        #     self.player.pos.y += abs(self.player.vel.y)
        #     for plat in self.platforms:
        #         plat.rect.y += abs(self.player.vel.y / 8)
        # if self.player.rect.top == HEIGHT / 28:
        #     self.player.pos.y -= abs(self.player.vel.y)
        #     for plat in self.platforms:
        #         plat.rect.y -= abs(self.player.vel.y / 8)

    def draw(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def start_screen(self):
        pass

    def gameover_screen(self):
        pass

game = Game()
game.start_screen()

while game.running:
    game.new()
    game.gameover_screen()

pygame.quit()

 







    