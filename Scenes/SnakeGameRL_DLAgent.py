from .Scene import Scene
import pygame
from typing import Self
import numpy as np
from Games.SnakeGameLogic import SnakeGame, InputAction, BlockState
from Singlton import GAME_MANAGER
from UI.Button import Button

import torch
import random
from collections import deque

# Import your model and trainer.
from ModelHelperFunctions.QTrainer import Linear_QNet, QTrainer
from PlotHelperFunctions.LineGraph import plot

# Hyperparameters for DQN.
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

# Global block size; set by set_scale.
block_size = 0

###############################################################################
# Deep RL Agent using a Deep Q-Network
###############################################################################
class DeepRLAgent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0   # randomness factor (will decay with games)
        self.gamma = 0.9   # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # stores past experiences
        # Input size of 11 (see get_state below), one hidden layer of 256 units, output size 3.
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game: SnakeGame):
        """
        Returns an 11-dimensional state representation.
        Assumes a fixed block size of 20 for positional offsets.
        """
        head = game.snake[0]
        # These points are offset by 20 (i.e. one block) in each direction.
        point_l = (head[0] - 20, head[1])
        point_r = (head[0] + 20, head[1])
        point_u = (head[0], head[1] - 20)
        point_d = (head[0], head[1] + 20)
        
        # Check current movement direction.
        dir_l = game.direction == InputAction.Left
        dir_r = game.direction == InputAction.Right
        dir_u = game.direction == InputAction.Up
        dir_d = game.direction == InputAction.Down
        
        state = [
            # Danger straight: if going right, check right; if left, check left; etc.
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right: assume turning right relative to current direction.
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left: assume turning left relative to current direction.
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Current move direction.
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location relative to head.
            game.food[0] < head[0],  # food to the left
            game.food[0] > head[0],  # food to the right
            game.food[1] < head[1],  # food above
            game.food[1] > head[1]   # food below
        ]
        
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        """Stores the experience in memory."""
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        """Train on a batch from the memory."""
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # random batch
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        """Train on a single step (short term memory)."""
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        """Returns the next move as a one-hot encoded list of length 3."""
        # Adjust epsilon to promote exploration early on.
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

###############################################################################
# Scene for the Deep RL Agent
###############################################################################
class SnakeGameRLAgent(Scene):
    def __init__(self):
        # Initialize the Deep RL agent and the game.
        self.agent = DeepRLAgent()
        self.game = SnakeGame("rl_agent")
        self.main_menu_button = None
        self.mouse_down_previous = False
        self.currentScore = 0
        self.last_input_process = 0
        self.speed = 30  # update frequency in seconds (steps per second)

    def process_game_step(self):
        # Get the current state from the game.
        state_old = self.agent.get_state(self.game)
        # Choose an action (a one-hot encoded vector of length 3).
        final_move = self.agent.get_action(state_old)
        # Play one step of the game; obtain reward, done flag, and score.
        reward, done, score = self.game.play_step(final_move)
        state_new = self.agent.get_state(self.game)
        # Train on this individual step.
        self.agent.train_short_memory(state_old, final_move, reward, state_new, done)
        # Remember the experience.
        self.agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # Game over: reset the game and train on long memory.
            self.game.reset()
            self.agent.n_games += 1
            self.agent.train_long_memory()
            if score > self.currentScore:
                self.currentScore = score
                # Optionally save the model:
                self.agent.model.save()
            print(f'Game {self.agent.n_games} Score {score}')

    def process_input(self, dt: float):
        if self.game.is_dead:
            self.game.reset()
            return

        if dt == 0:
            self.process_game_step()
            return

        self.last_input_process += dt
        if self.last_input_process >= 1 / self.speed:
            self.last_input_process = 0
            self.process_game_step()

        # Check for button clicks (e.g. Main Menu).
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed and not self.mouse_down_previous:
            mouse_pos = pygame.mouse.get_pos()
            if (self.main_menu_button is not None and 
                self.main_menu_button.rect.collidepoint(mouse_pos)):
                self.main_menu_button.on_click()
        self.mouse_down_previous = mouse_pressed

    def render_scene(self, screen: pygame.Surface):
        # Clear the screen.
        screen.fill("black")
        
        # --- Define grid drawing area ---
        game_offset_x = 10
        game_offset_y = 10
        game_width = self.game.cols * block_size
        game_height = self.game.rows * block_size

        # --- Draw game grid ---
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
        
        # --- Draw border around grid ---
        border_padding = 5
        border_rect = pygame.Rect(
            game_offset_x - border_padding,
            game_offset_y - border_padding,
            game_width + 2 * border_padding,
            game_height + 2 * border_padding
        )
        pygame.draw.rect(screen, "white", border_rect, 3)

        # --- Draw game stats below the grid ---
        stats_offset_y = game_offset_y + game_height + 10
        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
        time_text = font.render(f"Time: {self.game.get_elapsed_time():.1f}s", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {self.game.get_high_score()}", True, (255, 255, 255))
        screen.blit(score_text, (game_offset_x, stats_offset_y))
        screen.blit(time_text, (game_offset_x, stats_offset_y + 30))
        screen.blit(high_score_text, (game_offset_x, stats_offset_y + 60))
        
        # --- Draw the Main Menu Button ---
        button_width = 200
        button_height = 50
        menu_x = game_offset_x + game_width - button_width
        menu_y = stats_offset_y
        if self.main_menu_button is None:
            self.main_menu_button = Button(label="Main Menu", callback=self.load_main_menu)
        self.main_menu_button.rect = pygame.Rect(menu_x, menu_y, button_width, button_height)
        self.main_menu_button.draw(screen)

    def set_scale(self, width: int):
        global block_size
        block_size = (width - 20) / self.game.cols

    def load_main_menu(self):
        from Scenes import MainMenuScene as mm
        new_scene = mm.MainMenuScene()
        GAME_MANAGER.changeScene(new_scene)
