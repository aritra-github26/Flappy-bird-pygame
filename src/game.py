import pygame
import os
import sys

from src.bird import Bird
from src.pipe import Pipe

# Sound effects will be loaded after pygame.init()
SOUND_WING = None
SOUND_HIT = None
SOUND_POINT = None




class Game:
    def __init__(self):
        self.width = 288
        self.height = 512
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        # Initialize sound effects after pygame.init()
        global SOUND_WING, SOUND_HIT, SOUND_POINT
        SOUND_WING = pygame.mixer.Sound(os.path.join("sound", "sfx_wing.wav"))
        SOUND_HIT = pygame.mixer.Sound(os.path.join("sound", "sfx_hit.wav"))
        SOUND_POINT = pygame.mixer.Sound(os.path.join("sound", "sfx_point.wav"))
        
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()


        self.bird = Bird()
        self.pipes = []
        self.running = True
        self.score = 0
        self.background = pygame.image.load(os.path.join("assets", "background-day.png"))
        self.base = pygame.image.load(os.path.join("assets", "base.png"))
        self.base_x = 0
        self.pipe_spawn_time = 120
        self.pipe_timer = 0


    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.jump()
                    SOUND_WING.play()


    def update(self):
        self.bird.update()
        self.base_x = (self.base_x - 2) % -48
        
        # Update pipes
        for pipe in self.pipes:
            pipe.move()
            if pipe.x + pipe.pipe_top.get_width() < 0:
                self.pipes.remove(pipe)
        
        # Spawn new pipes
        self.pipe_timer += 1
        if self.pipe_timer > self.pipe_spawn_time:
            self.pipes.append(Pipe(self.width))
            self.pipe_timer = 0
        
        # Check if bird has fallen below the screen
        if self.bird.rect.y > self.height:
            SOUND_HIT.play()
            self.running = False
            self.show_game_over()
            return
            
        # Check for scoring and collisions
        for pipe in self.pipes:
            if not pipe.passed and pipe.x + pipe.pipe_top.get_width() < self.bird.rect.x:
                pipe.passed = True
                self.score += 1
                SOUND_POINT.play()
                
            if pipe.collide(self.bird):
                SOUND_HIT.play()
                self.running = False
                self.show_game_over()





    def render(self):
        self.window.blit(self.background, (0, 0))
        
        for pipe in self.pipes:
            pipe.draw(self.window)
            
        self.bird.draw(self.window)
        
        # Draw base
        self.window.blit(self.base, (self.base_x, self.height - self.base.get_height()))
        self.window.blit(self.base, (self.base_x + self.base.get_width(), self.height - self.base.get_height()))
        
        # Draw score
        font = pygame.font.SysFont("Arial", 30)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.window.blit(score_text, (10, 10))
        
        pygame.display.update()

    def show_game_over(self):
        # Load game over image
        game_over_img = pygame.image.load(os.path.join("assets", "gameover.png"))
        button_font = pygame.font.SysFont("Arial", 30)


        retry_text = button_font.render("Retry", True, (0, 0, 0))
        exit_text = button_font.render("Exit", True, (0, 0, 0))
        
        # Create button rectangles
        retry_rect = pygame.Rect(
            (self.width - 150) // 2,
            (self.height - 50) // 2,
            150, 50
        )
        exit_rect = pygame.Rect(
            (self.width - 150) // 2,
            (self.height - 50) // 2 + 70,
            150, 50
        )
        
        while True:
            # Draw game over screen
            self.window.blit(self.background, (0, 0))
            
            # Draw game over image
            self.window.blit(game_over_img, (
                (self.width - game_over_img.get_width()) // 2,
                (self.height - game_over_img.get_height()) // 2 - 100
            ))

            # Draw score
            score_text = button_font.render(f"Scores: {self.score}", True, (0, 0, 0))
            self.window.blit(score_text, (
                (self.width - score_text.get_width()) // 2,
                (self.height - game_over_img.get_height()) // 2 - 50
            ))





            
            # Draw buttons
            pygame.draw.rect(self.window, (200, 200, 200), retry_rect)
            pygame.draw.rect(self.window, (200, 200, 200), exit_rect)
            
            # Draw button text
            self.window.blit(retry_text, (
                retry_rect.x + (retry_rect.width - retry_text.get_width()) // 2,
                retry_rect.y + (retry_rect.height - retry_text.get_height()) // 2
            ))
            self.window.blit(exit_text, (
                exit_rect.x + (exit_rect.width - exit_text.get_width()) // 2,
                exit_rect.y + (exit_rect.height - exit_text.get_height()) // 2
            ))

            
            pygame.display.update()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if retry_rect.collidepoint(mouse_pos):
                        self.__init__()
                        self.run()
                        return
                    if exit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
