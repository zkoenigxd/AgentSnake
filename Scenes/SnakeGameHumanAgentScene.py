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
        self.main_menu_button = None
        self.mouse_down_previous = False
        self.game_manager = GAME_MANAGER
    
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
        if self.game is not None:
            if self.game.is_dead:
                self.end_game(screen)
            else:
                # Fill the background.
                screen.fill("black")
                
                # --- Define the grid drawing area ---
                # These offsets ensure that the grid is not drawn at the very edge,
                # leaving room for a border and score readouts.
                game_offset_x = 10
                game_offset_y = 10
                game_width = self.game.cols * block_size
                game_height = self.game.rows * block_size
                
                # --- Draw the grid blocks ---
                # Adjust each block's position based on the game area offsets.
                for x, row in enumerate(self.game.state_arr):
                    for y, block in enumerate(row):
                        rect = pygame.Rect(
                            game_offset_x + y * block_size,
                            game_offset_y + x * block_size,
                            block_size,
                            block_size
                        )
                        if block == BlockState.Snake:
                            pygame.draw.rect(screen, "white", rect, 0, 3)
                        elif block == BlockState.Food:
                            pygame.draw.rect(screen, "red", rect, 0, 3)
                        elif block == BlockState.Obsticle:
                            pygame.draw.rect(screen, "green", rect, 0, 3)
                
                # --- Draw a border around the grid ---
                # The border is drawn with a padding so it doesn't overlap the grid blocks.
                border_padding = 5  # adjust as needed
                border_rect = pygame.Rect(
                    game_offset_x - border_padding,
                    game_offset_y - border_padding,
                    game_width + 2 * border_padding,
                    game_height + 2 * border_padding
                )
                pygame.draw.rect(screen, "white", border_rect, 3)
                
                # --- Draw the score readouts outside the grid ---
                # Here, we choose to render the score information below the grid.
                stats_offset_y = game_offset_y + game_height + 10
                font = pygame.font.SysFont("Arial", 24)
                score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
                time_text = font.render(f"Time: {self.game.get_elapsed_time():.1f}s", True, (255, 255, 255))
                high_score_text = font.render(f"High Score: {self.game.get_high_score()}", True, (255, 255, 255))
                
                screen.blit(score_text, (game_offset_x, stats_offset_y))
                screen.blit(time_text, (game_offset_x, stats_offset_y + 30))
                screen.blit(high_score_text, (game_offset_x, stats_offset_y + 60))
                
    def end_game(self: Self, screen: pygame.Surface):
        # Fill the background with a solid color.
        screen.fill("red")
        
        # Obtain screen dimensions.
        screen_width, screen_height = screen.get_size()
        
        # Display game over text and stats in the upper half of the screen.
        font = pygame.font.SysFont("Arial", 48)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        font_small = pygame.font.SysFont("Arial", 24)
        score_text = font_small.render(f"Score: {self.game.score}", True, (255, 255, 255))
        time_text = font_small.render(f"Time: {self.game.get_elapsed_time():.1f}s", True, (255, 255, 255))
        high_score_text = font_small.render(f"High Score: {self.game.get_high_score()}", True, (255, 255, 255))
        total_time_text = font_small.render(f"Total Time: {self.game.get_total_time():.1f}s", True, (255, 255, 255))
        
        # Center the game over text near the top half.
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 150))
        screen.blit(game_over_text, game_over_rect)
        
        # Place the stats below the "Game Over" text but away from the game area.
        stats_y = game_over_rect.bottom + 10
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, stats_y))
        screen.blit(time_text, (screen_width // 2 - time_text.get_width() // 2, stats_y + 40))
        screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, stats_y + 80))
        screen.blit(total_time_text, (screen_width // 2 - total_time_text.get_width() // 2, stats_y + 120))

        # --- Create/reset buttons with updated positions ---
        # Restart Button:
        button_width = 200
        button_height = 50
        window_width, window_height = screen.get_size()
        y_position = window_height // 1.5 - button_height // 2
        restart_x = (screen_width - button_width) // 2
        # Position the restart button below the stats.
        restart_y = y_position
        if self.restart_button is None:
            self.restart_button = Button(
                label="Restart Game",
                callback=self.restart_game
            )
        self.restart_button.rect = pygame.Rect(restart_x, restart_y, button_width, button_height)
        
        # Main Menu Button:
        menu_y = restart_y + button_height + 10  # position below the restart button
        if self.main_menu_button is None:
            self.main_menu_button = Button(
                label="Main Menu",
                callback=self.load_main_menu
            )
        self.main_menu_button.rect = pygame.Rect(restart_x, menu_y, button_width, button_height)
        
        # Draw the buttons.
        self.restart_button.draw(screen)
        self.main_menu_button.draw(screen)
        
        # Check for button clicks.
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed and not self.mouse_down_previous:
            mouse_pos = pygame.mouse.get_pos()
            if self.restart_button.rect.collidepoint(mouse_pos):
                self.restart_button.on_click()
            if self.main_menu_button.rect.collidepoint(mouse_pos):
                self.main_menu_button.on_click()
        self.mouse_down_previous = mouse_pressed

    def restart_game(self):
        """Reset the game when the restart button is clicked"""
        self.game.reset()
        self.last_input_process = 0

    def load_main_menu(self):
        from Scenes import MainMenuScene as mm
        new_scene = mm.MainMenuScene()
        self.game_manager.changeScene(new_scene)

    def set_scale(self: Self, width : int):
        global block_size 
        block_size = (width - 20) / self.game.cols