import pygame
import get_names

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path, scale=1.0):
        super().__init__()
        image = pygame.image.load(image_path).convert_alpha()
        if scale != 1.0:
            width = int(image.get_width() * scale)
            height = int(image.get_height() * scale)
            image = pygame.transform.scale(image, (width, height))
        self.image = image
        self.rect = self.image.get_rect()
        self.health = 100
        self.damage = 10
        self.name = get_names.get_name()
        self.change_x = 0
        self.change_y = 0

    def setup(self):
        self.rect.x = 0
        self.rect.y = 0
        self.change_x = 0
        self.change_y = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.top - 10))
        surface.blit(text, text_rect)

    def update(self, *args):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

    def hit(self):
        self.health -= self.damage