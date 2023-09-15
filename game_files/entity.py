import pygame


class Entity:
    def __init__(
            self,
            x: float,
            y: float, speed: float,
            sprite: pygame.Surface
    ):
        self.x = x
        self.y = y
        self.speed = speed
        self.sprite = sprite

    def update(self, delta_time):
        pass

    def render(self, screen: pygame.Surface):
        pass
