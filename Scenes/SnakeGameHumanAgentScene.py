from .Scene import Scene
from typing import Self
import pygame
from Games import SnakeGameLogic
from Games.SnakeGameLogic import BlockState, InputAction
from Singlton import GAME_MANAGER
from UI.Button import Button

class SnakeGameHumanAgentScene(Scene):

    def __init__(self):
        self.speed = 10 # input processes per second
        self.last_input_process = 0
        self.game = SnakeGameLogic.SnakeGame("human")
        self.restart_button = None
        self.mouse_down_previous = False
    
    def collect_input(self: Self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.game.set_action(InputAction.Up)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.game.set_action(InputAction.Down)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.game.set_action(InputAction.Left)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.game.set_action(InputAction.Right)
    
    def process_input(self: Self, dt: float):
        # dt is delta time in seconds since last frame, used for framerate-independent input processing.
        if dt == 0:
            self.game.process_action()
            return
        self.last_input_process += dt
        if self.last_input_process >= 1 / self.speed:
            self.last_input_process = 0
            self.game.process_action()


    def set_input_pause(context = GAME_MANAGER.scene.game):
        if pygame.MOUSEBUTTONUP:
            mouse_press_location = pygame.mouse.get_pos()
        return mouse_press_location
    
    def render_scene(self: Self, screen: pygame.Surface):
        if self.game != None:
            if self.game.is_dead == True:
                self.end_game(screen)
            else:
                screen.fill("black")
                for x, row in enumerate(self.game.state_arr):
                    for y, block in enumerate(row):
                        if block == BlockState.Snake:
                            pygame.draw.rect(screen, "white", pygame.Rect(y * block_size, x * block_size,block_size,block_size), 0, 3)
                        if block == BlockState.Food:
                            pygame.draw.rect(screen, "red", pygame.Rect(y * block_size, x * block_size,block_size,block_size), 0, 3)
                        if block == BlockState.Obsticle:
                            pygame.draw.rect(screen, "green", pygame.Rect(y * block_size, x * block_size,block_size,block_size), 0, 3)
                
                # Display game stats
                font = pygame.font.SysFont("Arial", 24)
                score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
                time_text = font.render(f"Time: {self.game.get_elapsed_time():.1f}s", True, (255, 255, 255))
                high_score_text = font.render(f"High Score: {self.game.get_high_score()}", True, (255, 255, 255))
                
                # Position stats in top-left corner with 10px padding
                screen.blit(score_text, (10, 10))
                screen.blit(time_text, (10, 40))
                screen.blit(high_score_text, (10, 70))

    def end_game(self: Self, screen: pygame.Surface):
        screen.fill("red")
        
        # Display game over text and stats
        font = pygame.font.SysFont("Arial", 48)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
        time_text = font.render(f"Time: {self.game.get_elapsed_time():.1f}s", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {self.game.get_high_score()}", True, (255, 255, 255))
        total_time_text = font.render(f"Total Time: {self.game.get_total_time():.1f}s", True, (255, 255, 255))

        
        screen_width, screen_height = screen.get_size()
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 150))
        score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        time_rect = time_text.get_rect(center=(screen_width // 2, screen_height // 2))
        high_score_rect = high_score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        total_time_rect = total_time_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

        
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(time_text, time_rect)
        screen.blit(high_score_text, high_score_rect)
        screen.blit(total_time_text, total_time_rect)
        
        # Create restart button if it doesn't exist
        if self.restart_button is None:
            self.restart_button = Button(
                label="Restart Game",
                callback=self.restart_game
            )
            
            # Position the button in the center of the screen
            button_width = 200
            button_height = 50
            x_position = (screen_width - button_width) // 2
            y_position = screen_height // 2 + 200  # Moved down to accommodate new stats
            self.restart_button.rect = pygame.Rect(x_position, y_position, button_width, button_height)
        
        # Draw the restart button
        self.restart_button.draw(screen)
        
        # Check for button clicks
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed and not self.mouse_down_previous:
            mouse_pos = pygame.mouse.get_pos()
            if self.restart_button.rect.collidepoint(mouse_pos):
                self.restart_button.on_click()
        self.mouse_down_previous = mouse_pressed

    def restart_game(self):
        """Reset the game when the restart button is clicked"""
        self.game.reset()
        self.last_input_process = 0

    def set_scale(self: Self, width : int):
        global block_size 
        block_size = width / self.game.cols