import pygame
import sys
from player import Player
from enemy import Enemy
from boss import Boss
import ee
from room import Room
from get_conf import get_conf

WIDTH, HEIGHT = get_conf("width"), get_conf("height")
FPS = get_conf("FPS")

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(get_conf("title"))
        self.clock = pygame.time.Clock()
        self.pressed_keys = []

    def setup(self):
        self.player = Player("src/assets/player.png", scale=0.5)
        self.enemies = [Enemy("src/assets/enemy.png", scale=0.5) for _ in range(get_conf("count_enemys"))]
        self.boss = Boss("src/assets/boss.png", scale=0.5)
        self.bg_color = (0, 0, 0)
        self.room = None
        self.load_room(get_conf("first_room"))


    def load_room(self, room_name):
        self.room = Room(room_name, WIDTH, HEIGHT, self.conf)
        print(f"Room {room_name} loaded with entities: {self.room.entities}")

    def run(self):
        print("Starting the game loop...")
        running = True
        print("Game loop is running...")
        while running:
            print("Processing events...")
            delta = self.clock.tick(FPS) / 1000.0  # seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.on_key_press(event.key)

            keys = pygame.key.get_pressed()
            self.update(keys, delta)
            self.room.update(delta)
            print("Drawing the screen...")
            self.on_draw()
            self.room.draw(self.screen)
            pygame.display.flip()
            print("Drawing the screen finished...")
        pygame.quit()
        sys.exit()

    def on_draw(self):
        self.screen.fill(self.bg_color)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.boss.draw(self.screen)
        pygame.display.flip()
    def update(self, keys, delta):
        self.player.update(keys, delta)
        for enemy in self.enemies:
            enemy.update()
        self.boss.update(delta)

        # Collision with enemies
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                enemy.hit()

    def on_key_press(self, key):
        self.pressed_keys.append(key)
        print("Key empfangen: ", key)
        if key == pygame.K_LEFT or key == pygame.K_a:
            self.player.change_x = -self.player.speed
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.player.change_x = self.player.speed
        elif key == pygame.K_SPACE:
            self.player.attack()
        if self.pressed_keys[:-10] == [pygame.K_w, pygame.K_w, pygame.K_s, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_a, pygame.K_d, pygame.K_b, pygame.K_a]:
            ee.open_ee()

def main():
    print("Welcome to the 2D Fighting Game!")
    game = Game()
    print("Setting up the game...")
    game.setup()
    print("Game setup complete. Starting the game loop...")
    game.run()
    print("Game loop has ended. Exiting the game...")

if __name__ == "__main__":
    main()