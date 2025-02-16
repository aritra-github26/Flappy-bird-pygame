import pygame
import random
import os

class Pipe:
    GAP = 100
    SPEED = 2

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.pipe_top = pygame.image.load(os.path.join("assets", "pipe-green.png"))
        self.pipe_bottom = pygame.transform.flip(self.pipe_top, False, True)
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randint(150, 300)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.SPEED

    def draw(self, window):
        window.blit(self.pipe_top, (self.x, self.top))
        window.blit(self.pipe_bottom, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = pygame.mask.from_surface(bird.images[bird.current_image])
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)
        
        top_offset = (self.x - bird.rect.x, self.top - round(bird.rect.y))
        bottom_offset = (self.x - bird.rect.x, self.bottom - round(bird.rect.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        return False
