import pygame

from game_files.scenes.scene_manager import Scene
from game_files.scenes.scene_manager import SceneManager


class StartScene(Scene):
    def __init__(
            self,
            manager: SceneManager,
            screen: pygame.Surface,
            sprites: dict
    ):
        super().__init__(manager, screen, sprites)
        self.font = pygame.font.SysFont("Arial", 36)
        self.text = "Press Space To Begin"
        self.text_x = 400
        self.text_y = 200

    def update(self):
        pass

    def render(self):
        # Clear screen
        self.screen.fill("black")

        self.screen.blit(
            self.font.render(self.text, True, "white"),
            (self.text_x, self.text_y)
        )

        # Update display
        pygame.display.update()

    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.manager.quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.manager.set_scene("main")
