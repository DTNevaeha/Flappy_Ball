import pygame
import random
import time


class Entity:
    def __init__(self, x: float, y: float, speed: float, sprite: pygame.Surface):
        self.x = x
        self.y = y
        self.speed = speed
        self.sprite = sprite

    def update(self, delta_time):
        pass

    def render(self, screen: pygame.Surface):
        pass


class Player(Entity):
    def __init__(
        self, x: float, y: float, speed: float, sprite: pygame.Surface, gravity: float
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


class Obstacle(Entity):
    # Nested class because we will be using multiple blocks
    class ObstacleBlock(Entity):
        def __init__(self, x: float, y: float, speed: float, sprite: pygame.Surface):
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
        gap_location: int,  # Number of blocks from the top of the screen where gap is located
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
        self.gap_range = (self.gap_location,
                          self.gap_location + self.gap_height)

        self.blocks = self.create_blocks()

        self.passed = False

    def create_blocks(self) -> list[ObstacleBlock]:
        obstacle_list = []
        current_block = 0
        for i in range(self.num_blocks):
            if i < self.gap_range[0] or i > self.gap_range[1]:
                # x value is all moving at once, but Y value gap changes. Current block tracks the current pixel value
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

        self.obstacles = []  # Contain all of the currently active obstacles on screen
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

        if self.new_obstacle_timer > self.frequency:  # Time to spawn a new obstacle
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
        screen.blit(self.font.render(
            self.text, True, "white"), (self.x, self.y))


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
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict):
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
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict):
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
                self.manager.quit_game()

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


class StartScene(Scene):
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict):
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
            self.font.render(
                self.text, True, "white"), (self.text_x, self.text_y)
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


class DeathScene(Scene):
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict):
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
            self.font.render(
                self.text, True, "white"), (self.text_x, self.text_y)
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
        sprites["obstacle"] = pygame.image.load(
            "gfx/block.png").convert_alpha()
        sprites["background"] = pygame.image.load("gfx/bg.png").convert_alpha()

        return sprites


run_game = Game()
run_game.run()
