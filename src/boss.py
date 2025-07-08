import pygame
import enemy

class Boss(enemy.Enemy):
    def __init__(self, image_path, scale=0.1):
        super().__init__(image_path, scale)
        self.health = 400
        self.damage = 4
        self.image = pygame.image.load(image_path).convert_alpha()
        width = int(self.image.get_width() * scale)
        height = int(self.image.get_height() * scale)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

    def update(self, delta_time):
        super().update()