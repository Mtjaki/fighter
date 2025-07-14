
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