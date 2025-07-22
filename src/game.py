import pygame
import sys
import os
from player import Player
from enemy import Enemy
from boss import Boss
import ee
from room import Room
from room_manager import RoomManager
from get_conf import get_conf

WIDTH, HEIGHT = get_conf("size")["width"], get_conf("size")["height"]
FPS = get_conf("FPS")
ASCII_CHARS = open("src/assets/ascii_chars.txt").read().strip()

def pixel_to_ascii(pixel):
    # Berechne die Helligkeit des Pixels
    brightness = sum(pixel) // 3  # Durchschnitt der RGB-Werte
    # Wandle die Helligkeit in ein ASCII-Zeichen um
    return ASCII_CHARS[brightness * len(ASCII_CHARS) // 256]

def frame_to_ascii(frame):
    ascii_image = ""
    for y in range(frame.get_height()):
        for x in range(frame.get_width()):
            pixel = frame.get_at((x, y))[:3]  # RGB-Werte
            ascii_char = pixel_to_ascii(pixel)
            # ANSI-Farbcodes für die Konsolenausgabe
            r, g, b = pixel
            ascii_image += f"\033[38;2;{r};{g};{b}m{ascii_char}"
        ascii_image += "\n"
    return ascii_image + "\033[0m"  # Zurücksetzen der Farben

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(get_conf("name"))
        self.clock = pygame.time.Clock()
        self.pressed_keys = []
        self.room_manager = RoomManager()  # Neuer Room Manager

    def setup(self):
        self.player = Player("src/assets/character.jpeg", scale=0.5)
        self.bg_color = (0, 0, 0)
        self.room = None
        self.load_room(get_conf("first_room"))
        print(self.room_manager.available_rooms)

    def load_room(self, room_name):
        """Lädt einen neuen Raum über den RoomManager"""
        print(f"Loading room: {room_name}")
        self.room = self.room_manager.load_room(room_name, WIDTH, HEIGHT)
        
        if self.room is None:
            print(f"Fehler: Raum '{room_name}' konnte nicht geladen werden!")
            return
        
        # Setze Spielerposition basierend auf Raumeingang
        self.player.rect.x = 100  # Standard-Startposition
        self.player.rect.y = 100
        
        print(f"Room {room_name} loaded with {len(self.room.entities)} entities")
        
        # Zeige Raum-Info an
        room_info = self.room_manager.get_room_info(room_name)
        if room_info:
            print(f"Raum: {room_info['title']}")
            print(f"Ausgänge: {', '.join(room_info['exits']) if room_info['exits'] else 'Keine'}")

    def run(self):
        print("Starting the game loop...")
        running = True
        print("Game loop is running...")
        while running:
            delta = self.clock.tick(FPS) / 1000.0  # seconds
            
            # Event-Verarbeitung
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.on_key_press(event.key)

            # Überprüfe Raumübergänge
            new_room = self.room.handle_events(events)
            if new_room:
                self.load_room(new_room)

            keys = pygame.key.get_pressed()
            self.update(keys, delta)
            self.room.update(delta)
            
            # Zeichnen
            self.on_draw()
            # Frame in ASCII umwandeln
            frame = pygame.surfarray.array3d(pygame.display.get_surface())
            ascii_art = frame_to_ascii(pygame.display.get_surface())

            # ASCII-Art ausgeben
            os.system('cls' if os.name == 'nt' else 'clear')
            print(ascii_art)
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()

    def on_draw(self):
        """Zeichnet das gesamte Spiel"""
        self.screen.fill(self.bg_color)
        
        # Zeichne den aktuellen Raum
        self.room.draw(self.screen)
        
        # Zeichne den Spieler
        self.player.draw(self.screen)
    def update(self, keys, delta):
        """Aktualisiert das Spiel"""
        self.player.update(keys, delta)

        # Kollisionen mit Raum-Entitäten
        enemies = self.room.get_enemies()
        for enemy in enemies:
            if self.player.rect.colliderect(enemy.rect):
                enemy.hit()
                # Optional: Entferne besiegte Feinde
                if hasattr(enemy, 'health') and enemy.health <= 0:
                    self.room.remove_entity(enemy)

        bosses = self.room.get_bosses()
        for boss in bosses:
            if self.player.rect.colliderect(boss.rect):
                boss.hit() if hasattr(boss, 'hit') else None

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