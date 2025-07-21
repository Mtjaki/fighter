import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, scale=1.0):
        super().__init__()
        image = pygame.image.load(image_path).convert_alpha()
        if scale != 1.0:
            size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, size)
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 5
        self.health = 100
        self.change_x = 0
        self.change_y = 0

    def update(self, keys, delta):
        self.change_x = 0
        self.change_y = 0

        if keys[pygame.K_LEFT]:
            self.change_x = -self.speed * delta
        elif keys[pygame.K_RIGHT]:
            self.change_x = self.speed * delta

        if keys[pygame.K_UP]:
            self.change_y = -self.speed * delta
        elif keys[pygame.K_DOWN]:
            self.change_y = self.speed * delta

        self.rect.x += int(self.change_x)
        self.rect.y += int(self.change_y)
    def draw(self, screen):
        pass
    def attack(self):
        # Placeholder for attack logic
        pass