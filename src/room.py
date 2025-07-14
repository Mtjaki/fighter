
import pygame
import sys
import json

from player import Player
from enemy import Enemy
from boss import Boss


class Room:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.entities = []
        self.exits = {}
        self.items = []
        self.background_color = (0, 0, 0)
        self.background_image = None
        
        # Lade Raum-Daten aus JSON
        with open(f"src/rooms/{name}.json", "r") as file:
            data = json.load(file)
            self.description = data.get("description", "")
            self.background_color = tuple(data.get("background_color", [0, 0, 0]))
            self.exits = data.get("exits", {})
            self.items = data.get("items", [])
            
            # Lade Hintergrundbild falls vorhanden
            if "background_image" in data:
                try:
                    self.background_image = pygame.image.load(f"src/assets/{data['background_image']}")
                    self.background_image = pygame.transform.scale(self.background_image, (width, height))
                except:
                    print(f"Warnung: Hintergrundbild {data['background_image']} konnte nicht geladen werden")
            
            self.entities = self.load_entities(data.get("entities", []))
        print(f"Room {self.name} initialized with {len(self.entities)} entities")

    def load_entities(self, entity_data):
        """Lädt Entitäten basierend auf den JSON-Daten"""
        entities = []
        for entity_info in entity_data:
            entity_type = entity_info.get("type")
            position = entity_info.get("position", [0, 0])
            
            if entity_type == "enemy":
                enemy = Enemy("src/assets/enemy.jpeg", scale=entity_info.get("scale", 0.5))
                enemy.rect.x, enemy.rect.y = position
                entities.append(enemy)
            elif entity_type == "boss":
                boss = Boss("src/assets/boss.png", scale=entity_info.get("scale", 0.5))
                boss.rect.x, boss.rect.y = position
                entities.append(boss)
            # Player wird normalerweise nicht hier erstellt, sondern in Game
            
        return entities

    def update(self, dt):
        """Aktualisiert alle Entitäten im Raum"""
        for entity in self.entities:
            if hasattr(entity, 'update'):
                entity.update(dt) if entity.__class__.__name__ == 'Boss' else entity.update()
        
    def draw(self, surface):
        """Zeichnet den Raum und alle Entitäten"""
        # Hintergrund zeichnen
        if self.background_image:
            surface.blit(self.background_image, (0, 0))
        else:
            surface.fill(self.background_color)
            
        # Entitäten zeichnen
        for entity in self.entities:
            if hasattr(entity, 'draw'):
                entity.draw(surface)

    def handle_events(self, events):
        """Verarbeitet Eingaben für den Raum"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Überprüfe Raumübergänge
                if event.key == pygame.K_UP and "north" in self.exits:
                    return self.exits["north"]
                elif event.key == pygame.K_DOWN and "south" in self.exits:
                    return self.exits["south"]
                elif event.key == pygame.K_LEFT and "west" in self.exits:
                    return self.exits["west"]
                elif event.key == pygame.K_RIGHT and "east" in self.exits:
                    return self.exits["east"]
        return None

    def add_entity(self, entity):
        """Fügt eine Entität zum Raum hinzu"""
        self.entities.append(entity)

    def remove_entity(self, entity):
        """Entfernt eine Entität aus dem Raum"""
        if entity in self.entities:
            self.entities.remove(entity)

    def get_enemies(self):
        """Gibt alle Feinde im Raum zurück"""
        return [entity for entity in self.entities if isinstance(entity, Enemy)]

    def get_bosses(self):
        """Gibt alle Bosse im Raum zurück"""
        return [entity for entity in self.entities if isinstance(entity, Boss)]