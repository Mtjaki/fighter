import pygame
import sys
from player import Player
from enemy import Enemy
from boss import Boss
from ee import EE

WIDTH, HEIGHT = 800, 600
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2D Fighting Game")
        self.clock = pygame.time.Clock()
        self.bg_color = (178, 190, 181)  # ASH_GREY approximation
        self.pressed_keys = []

    def setup(self):
        self.player = Player("./assets/character.jpeg", scale=0.5)
        self.ee = EE()
        self.enemies = []
        for i in range(5):
            enemy = Enemy("./assets/enemy.jpeg", scale=0.5)
            enemy.rect.x = 200 + i * 50
            enemy.rect.y = 200 + i * 50
            self.enemies.append(enemy)
        self.boss = Boss("./assets/boss.jpeg", scale=0.5)

        self.player.rect.x = 100
        self.player.rect.y = 100
        self.boss.rect.x = 500
        self.boss.rect.y = 500

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
            print("Drawing the screen...")
            self.on_draw()
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
            self.ee.open()

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