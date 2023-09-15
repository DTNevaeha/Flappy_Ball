import pygame


class Score:
    def __init__(self, x, y):
        self.font = pygame.font.SysFont("Calibri", 36)
        self.score = 0
        self.text = str(self.score)
        self.x = x
        self.y = y

    def add_score(self):
        self.score += 1

    def update(self) -> None:
        self.text = str(self.score)

    def render(self, screen: pygame.Surface):
        screen.blit(self.font.render(self.text, True, "white"),
                    (self.x, self.y))
