import pygame
import sys

# ASCII-Zeichen, die für die Umwandlung verwendet werden
ASCII_CHARS = "@%#*+=-:. "

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

# Pygame initialisieren
pygame.init()
screen = pygame.display.set_mode((640, 480))

# Hauptschleife
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Hier kannst du deinen Frame zeichnen
    screen.fill((0, 0, 0))  # Beispiel: Bildschirm schwarz füllen
    pygame.draw.circle(screen, (255, 0, 0), (320, 240), 100)  # Beispiel: roten Kreis zeichnen

    # Frame in ASCII umwandeln
    frame = pygame.surfarray.array3d(pygame.display.get_surface())
    ascii_art = frame_to_ascii(pygame.display.get_surface())

    # ASCII-Art ausgeben
    print(ascii_art)

    pygame.display.flip()
