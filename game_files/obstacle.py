import pygame

from game_files.entity import Entity


class Obstacle(Entity):
    # Nested class because we will be using multiple blocks
    class ObstacleBlock(Entity):
        def __init__(
                self,
                x: float,
                y: float,
                speed: float,
                sprite: pygame.Surface
        ):
            super().__init__(x, y, speed, sprite)
            self.rectangle = self.sprite.get_rect()

        def update(self, delta_time):
            self.x += self.speed * delta_time

            # Update rectangle
            self.rectangle.x = int(self.x)
            self.rectangle.y = int(self.y)

        def render(self, screen: pygame.Surface):
            screen.blit(self.sprite, (self.x, self.y))

    def __init__(
        self,
        x: float,
        y: float,
        speed: float,
        screen_height: int,
        gap_height: int,  # Number of blocks missing to form gap in walls
        # Number of blocks from the top of the screen where gap is located
        gap_location: int,
        sprite: pygame.Surface,
    ):
        super().__init__(x, y, speed, sprite)
        self.screen_height = screen_height
        self.gap_height = gap_height
        self.gap_location = gap_location
        self.BLOCK_SIZE = 48  # Obstacle block sprites

        # Calculate the number of blocks required to fill the screen
        # Do not 'hard code' as the screen size changes per person
        self.num_blocks = round(
            self.screen_height / self.BLOCK_SIZE
        )  # Round to not leave any floating numbers

        # Calculate gap
        self.gap_range = (
            self.gap_location,
            self.gap_location + self.gap_height
        )

        self.blocks = self.create_blocks()

        self.passed = False

    def create_blocks(self) -> list[ObstacleBlock]:
        obstacle_list = []
        current_block = 0
        for block in range(self.num_blocks):
            if block < self.gap_range[0] or block > self.gap_range[1]:
                # x value is all moving at once, but Y value gap changes.
                # Current block tracks the current pixel value
                obstacle_list.append(
                    Obstacle.ObstacleBlock(
                        self.x, current_block, self.speed, self.sprite
                    )
                )
            current_block += self.BLOCK_SIZE
        return obstacle_list

    def update(self, delta_time):
        self.x += self.speed * delta_time
        for block in self.blocks:
            block.update(delta_time)

    def render(self, screen: pygame.Surface):
        for block in self.blocks:
            block.render(screen)
