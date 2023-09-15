import pygame
import random

from game_files.player import Player
from game_files.obstacle import Obstacle


# Manages the obstacles and collision between obstacles and the player
class Environment:
    def __init__(
        self,
        player: Player,
        screen: pygame.Surface,
        sprites: dict,
        frequency: int,
        obstacle_speed: float,
        obstacle_gap: int,
    ):
        self.obstacle_speed = obstacle_speed
        self.obstacle_gap = obstacle_gap
        self.frequency = frequency
        self.screen = screen
        self.player = player
        self.sprites = sprites

        # Contain all of the currently active obstacles on screen
        self.obstacles = []
        self.obstacle_spawn_point = 1280  # spawn on far right of screen
        self.new_obstacle_timer = 0

        self.score_tracker = 0

    def add_obstacle(self, obstacle: Obstacle):
        self.obstacles.append(obstacle)

    def remove_obstacle(self):
        self.obstacles.pop(0)

    def update_obstacles(self, delta_time):
        for obstacle in self.obstacles:
            obstacle.update(delta_time)
            # Remove obstacles from game if they pass the left of the screen
            if obstacle.x < -200:
                self.remove_obstacle()

            # Adds score to the game if a obstacle passes the player, one time.
            if obstacle.x < self.player.x and not obstacle.passed:
                obstacle.passed = True
                self.score_tracker += 1

        # Time to spawn a new obstacle
        if self.new_obstacle_timer > self.frequency:
            gap = random.randint(2, 10)

            obstacle = Obstacle(
                self.obstacle_spawn_point,
                0,
                self.obstacle_speed,
                self.screen.get_height(),
                self.obstacle_gap,
                gap,
                self.sprites["obstacle"],
            )
            self.add_obstacle(obstacle)
            self.new_obstacle_timer = 0

        self.new_obstacle_timer += 1

    def update(self, delta_time):
        self.update_obstacles(delta_time)

    def render(self, screen: pygame.Surface):
        for obstacle in self.obstacles:
            obstacle.render(screen)
