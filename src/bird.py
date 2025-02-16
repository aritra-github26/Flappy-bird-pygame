import pygame
import os

class Bird:
    def __init__(self):
        self.images = [
            pygame.image.load(os.path.join("assets", "bluebird-downflap.png")),
            pygame.image.load(os.path.join("assets", "bluebird-midflap.png")),
            pygame.image.load(os.path.join("assets", "bluebird-upflap.png"))
        ]
        self.current_image = 0
        self.rect = self.images[0].get_rect(center=(50, 256))
        self.velocity = 0
        self.gravity = 0.5
        self.flap_strength = -6  # Reduced jump strength for shorter jumps

        self.animation_speed = 0.2
        self.animation_counter = 0

    def jump(self):
        self.velocity = self.flap_strength

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity
        
        # Prevent bird from flying above the screen
        if self.rect.y < 0:
            self.rect.y = 0
            self.velocity = 0
            
        # Animation
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.animation_counter = 0


    def draw(self, window):
        window.blit(self.images[self.current_image], self.rect)
