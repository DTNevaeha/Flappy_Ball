import pygame
import time

from game_files.environment import Environment
from game_files.player import Player
from game_files.score import Score


class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.quit = False

    def initialize(self, scenes: dict, starting_scene: str):
        self.scenes = scenes
        self.current_scene = self.scenes[starting_scene]

    def set_scene(self, new_scene: str):
        self.current_scene = self.scenes[new_scene]

    def get_scene(self):
        return self.current_scene

    def quit_game(self):
        self.quit = True

    def reset_main(self):
        # Sets a default main scene
        new_scene = MainScene(
            self, self.scenes["main"].screen, self.scenes["main"].sprites
        )
        # Reset old main scene for a new main scene so you can restart
        self.scenes["main"] = new_scene


class Scene:
    def __init__(
            self,
            manager: SceneManager,
            screen: pygame.Surface,
            sprites: dict
    ):
        self.manager = manager
        self.screen = screen
        self.sprites = sprites

    def update(self):
        pass

    def render(self):
        pass

    def poll_events(self):
        pass


class MainScene(Scene):
    def __init__(
            self,
            manager: SceneManager,
            screen: pygame.Surface,
            sprites: dict
    ):
        super().__init__(manager, screen, sprites)

        self.previous_time = None

        # GAME CONSTANTS
        self.GRAVITY = 1700
        self.PLAYER_SPEED = 200
        self.JUMP = -450
        self.OBSTACLE_FREQUENCY = 1600
        self.OBSTACLE_SPEED = -200
        self.OBSTACLE_GAP = 2

        # Setup the initial player in the center of the screen
        self.player = Player(
            self.screen.get_width() / 2,
            self.screen.get_height() / 2,
            self.PLAYER_SPEED,
            self.sprites["player"],
            self.GRAVITY,
        )

        # Setup the screen
        self.environment = Environment(
            self.player,
            self.screen,
            self.sprites,
            self.OBSTACLE_FREQUENCY,
            self.OBSTACLE_SPEED,
            self.OBSTACLE_GAP,
        )

        self.score = Score(self.screen.get_width() / 2, 50)

    def update(self):
        if self.previous_time is None:  # This is the first time running
            self.previous_time = time.time()

        # Delta time
        now = time.time()
        delta_time = now - self.previous_time
        self.previous_time = now

        self.player.update(delta_time)
        self.environment.update(delta_time)

        # Check death conditions
        if self.player_collision() or self.player.y > self.screen.get_height():
            self.player.play_death_sound()
            self.manager.set_scene("death")

        if self.environment.score_tracker > self.score.score:
            self.score.add_score()

        self.score.update()

    def render(self):
        self.screen.fill("black")
        self.screen.blit(self.sprites["background"], (0, 0))

        self.player.render(self.screen)
        self.environment.render(self.screen)
        self.score.render(self.screen)

        pygame.display.update()

    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Scene.quit_game()

            # Key commands
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.speed = self.JUMP
                    self.player.play_jump_sound()

    def player_collision(self) -> bool:
        for object in self.environment.obstacles:
            for block in object.blocks:
                if block.rectangle.colliderect(self.player.rectangle):
                    return True
        return False
