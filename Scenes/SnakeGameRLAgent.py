import pygame  
import numpy as np
from .Scene import Scene
from Games.SnakeGameLogic import SnakeGame, InputAction, BlockState
from Singlton import GAME_MANAGER


class SnakeGameRLAgent(Scene):
    def __init__(self):
        # Initialize the Snake game
        self.game = SnakeGame("rl_agent")


        # Q-table for storing state-action values
        self.q_table = {}


        # Learning parameters
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.5
        self.epsilon_decay = 0.995
        self.min_epsilon = 0.01


        # Actions the agent can take
        self.actions = [InputAction.Up, InputAction.Down, InputAction.Left, InputAction.Right]


        # Time tracking for limiting agent speed
        self.last_action_time = 0


    def get_state(self):
        """
        Encodes the current game state into a tuple that can be used as a key in the Q-table.
        """
        head_x, head_y = self.game.head_location
        food_x, food_y = [(x, y) for x, row in enumerate(self.game.state_arr) for y, block in enumerate(row) if block == BlockState.Food][0]
        return (head_x, head_y, food_x, food_y)


    def choose_action(self, state):
        """
        Chooses an action based on the epsilon-greedy policy.
        """
        if np.random.rand() < self.epsilon:
            # Explore: choose a random action
            return np.random.choice(self.actions)
        else:
            # Exploit: choose the action with the highest Q-value
            if state in self.q_table:
                return max(self.q_table[state], key=self.q_table[state].get)
            else:
                # If the state is not in the Q-table, initialize it
                self.q_table[state] = {action: 0 for action in self.actions}
                return np.random.choice(self.actions)


    def update_q_table(self, state, action, reward, next_state):
        """
        Updates the Q-value for the given state-action pair using the Q-learning formula.
        """
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in self.actions}
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0 for a in self.actions}


        # Q-learning formula
        old_value = self.q_table[state][action]
        next_max = max(self.q_table[next_state].values())
        new_value = old_value + self.learning_rate * (reward + self.discount_factor * next_max - old_value)
        self.q_table[state][action] = new_value


    def collect_input(self):
        """
        Collects input by choosing an action based on the current state.
        """
        state = self.get_state()
        action = self.choose_action(state)
        self.game.set_action(action)


    def process_input(self, dt: float):
        """
        Processes the chosen action and updates the Q-table.
        """
        if self.game.is_dead:
            self.game = SnakeGame("rl_agent")
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
            return


        # Get the current state
        state = self.get_state()


        # Perform the action
        self.game.process_action()


        # Get the next state and reward
        next_state = self.get_state()
        reward = self.get_reward()


        # Update the Q-table
        self.update_q_table(state, self.game.action, reward, next_state)


    def get_reward(self):
        """
        Calculates the reward for the current state.
        """
        if self.game.is_dead:
            return -10  # Negative reward for dying
        elif self.game.state_arr[self.game.head_location[0]][self.game.head_location[1]] == BlockState.Food:
            return 10  # Positive reward for eating food
        else:
            return -1  # Small negative reward for each step to encourage faster solutions


    def render_scene(self, screen):
        """
        Renders the game on the screen.
        """
        screen.fill("black")
        for x, row in enumerate(self.game.state_arr):
            for y, block in enumerate(row):
                if block == BlockState.Snake:
                    pygame.draw.rect(screen, "white", pygame.Rect(y * block_size, x * block_size, block_size, block_size), 0, 3)
                if block == BlockState.Food:
                    pygame.draw.rect(screen, "red", pygame.Rect(y * block_size, x * block_size, block_size, block_size), 0, 3)


    def set_scale(self, width: int):
        """
        Sets the scale of the game grid.
        """
        global block_size
        block_size = width / self.game.cols