import pygame

from game_files.scenes.death_scene import DeathScene
from game_files.scenes.scene_manager import MainScene
from game_files.scenes.scene_manager import SceneManager
from game_files.scenes.start_scene import StartScene


class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((1280, 720))
        self.sprites = self.load_sprites()

        # Sets which scenes (or screens) are avaliable to use
        self.scene_manager = SceneManager()
        scenes = {
            "main": MainScene(self.scene_manager, self.screen, self.sprites),
            "start": StartScene(self.scene_manager, self.screen, self.sprites),
            "death": DeathScene(self.scene_manager, self.screen, self.sprites),
        }
        # Sets the initial dispaly screen
        self.scene_manager.initialize(scenes, "start")

        # Play music
        pygame.mixer.music.load("sfx/music.wav")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()

    # Manages and keeps everything running
    def run(self):
        while self.running:
            self.scene_manager.current_scene.poll_events()
            self.scene_manager.current_scene.update()
            self.scene_manager.current_scene.render()

            if self.scene_manager.quit is True:
                self.running = False

        pygame.quit()

    def load_sprites(self) -> dict:
        sprites = {}

        sprites["player"] = pygame.image.load("gfx/ball.png").convert_alpha()
        sprites["obstacle"] = pygame.image.load("gfx/block.png").convert_alpha()  # noqa: E501  This ignores line too long with flake8
        sprites["background"] = pygame.image.load("gfx/bg.png").convert_alpha()

        return sprites


run_game = Game()
run_game.run()
