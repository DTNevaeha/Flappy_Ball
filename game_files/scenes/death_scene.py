import pygame

from game_files.scenes.scene_manager import Scene
from game_files.scenes.scene_manager import SceneManager


class DeathScene(Scene):
    def __init__(
            self,
            manager: SceneManager,
            screen: pygame.Surface,
            sprites: dict
    ):
        super().__init__(manager, screen, sprites)
        self.font = pygame.font.SysFont("Arial", 36)
        self.text = "You Died! Press Space to Restart"
        self.text_x = 400
        self.text_y = 200

    def update(self):
        pass

    def render(self):
        # Clear the screen
        self.screen.fill((59, 3, 3))

        self.screen.blit(
            self.font.render(self.text, True, "white"),
            (self.text_x, self.text_y)
        )

        # Update the display
        pygame.display.update()

    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.manager.quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.manager.reset_main()
                    self.manager.set_scene("main")
