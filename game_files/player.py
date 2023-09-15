import pygame

from game_files.entity import Entity


class Player(Entity):
    def __init__(
        self,
        x: float,
        y: float,
        speed: float,
        sprite: pygame.Surface,
        gravity: float
    ):
        super().__init__(x, y, speed, sprite)
        self.gravity = gravity
        self.rectangle = self.sprite.get_rect()

        # Sounds
        self.jump_sound = pygame.mixer.Sound("sfx/bounce.wav")
        self.jump_sound.set_volume(0.1)
        self.death_south = pygame.mixer.Sound("sfx/death.wav")
        self.death_south.set_volume(0.5)

    def update(self, delta_time):
        self.y += self.speed * delta_time
        self.speed += self.gravity * delta_time

        # Prevent the player from going above the screen
        if self.y < 0:
            self.y = 0

        # Update rect
        self.rectangle.x = int(self.x)
        self.rectangle.y = int(self.y)

    def render(self, screen: pygame.Surface):
        screen.blit(self.sprite, (self.x, self.y))

    def play_jump_sound(self):
        self.jump_sound.play()

    def play_death_sound(self):
        self.death_south.play()
