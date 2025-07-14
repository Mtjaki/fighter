
import pygame
import sys
import json

from scene import Scene
from player import Player
from enemy import Enemy
from boss import Boss


class Room(Scene):
    def __init__(self, name, width, height, conf):
        super().__init__()
        self.name = name
        self.width = width
        self.height = height
        self.conf = conf
        self.entities = []
        with open(f"src/rooms/{name}.json", "r") as file:
            data = json.load(file)
            self.description = data.get("description", "")
            self.entities = self.load_entities(data.get("entities", []))
        print(f"Room {self.name} initialized with width {self.width} and height {self.height}")
        pass
    
    def update(self, dt):
        # Raum-spezifische Logik
        for entity in self.entities:
            entity.update(dt)
        print(f"Updating room: {self.name} with dt: {dt}")
        pass

    def draw(self, surface):
        # Raum zeichnen
        surface.fill((0, 0, 0))
        for entity in self.entities:
            entity.draw(surface)
        pass

    def handle_events(self, events):
        # Eingaben verarbeiten
        pass