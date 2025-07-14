import pygame
import json
import os
from room import Room

class RoomManager:
    """Verwaltet alle Räume und Übergänge im Spiel"""
    
    def __init__(self, room_directory="src/rooms/"):
        self.room_directory = room_directory
        self.current_room = None
        self.available_rooms = self._scan_available_rooms()
        self.room_cache = {}  # Cache für bereits geladene Räume
        
    def _scan_available_rooms(self):
        """Scannt alle verfügbaren Raum-JSON-Dateien"""
        rooms = []
        if os.path.exists(self.room_directory):
            for file in os.listdir(self.room_directory):
                if file.endswith('.json'):
                    room_name = file[:-5]  # Entferne .json
                    rooms.append(room_name)
        return rooms
    
    def load_room(self, room_name, width, height):
        """Lädt einen Raum (mit Caching für bessere Performance)"""
        if room_name not in self.available_rooms:
            print(f"Warnung: Raum '{room_name}' nicht gefunden!")
            return None
            
        # Verwende Cache wenn verfügbar
        cache_key = f"{room_name}_{width}_{height}"
        if cache_key in self.room_cache:
            self.current_room = self.room_cache[cache_key]
        else:
            self.current_room = Room(room_name, width, height)
            self.room_cache[cache_key] = self.current_room
            
        return self.current_room
    
    def get_current_room(self):
        """Gibt den aktuellen Raum zurück"""
        return self.current_room
    
    def get_room_info(self, room_name):
        """Gibt Informationen über einen Raum zurück, ohne ihn zu laden"""
        try:
            with open(f"{self.room_directory}{room_name}.json", "r") as file:
                data = json.load(file)
                return {
                    "title": data.get("title", room_name),
                    "description": data.get("description", ""),
                    "entity_count": len(data.get("entities", [])),
                    "exits": list(data.get("exits", {}).keys())
                }
        except FileNotFoundError:
            return None
    
    def list_available_rooms(self):
        """Listet alle verfügbaren Räume auf"""
        return self.available_rooms.copy()
    
    def validate_room_connections(self):
        """Überprüft, ob alle Raumverbindungen gültig sind"""
        issues = []
        for room_name in self.available_rooms:
            try:
                with open(f"{self.room_directory}{room_name}.json", "r") as file:
                    data = json.load(file)
                    exits = data.get("exits", {})
                    for direction, target_room in exits.items():
                        if target_room not in self.available_rooms:
                            issues.append(f"Raum '{room_name}' verweist auf nicht existenten Raum '{target_room}' ({direction})")
            except Exception as e:
                issues.append(f"Fehler beim Lesen von Raum '{room_name}': {e}")
        return issues
    
    def create_room_template(self, room_name):
        """Erstellt eine Vorlage für einen neuen Raum"""
        template = {
            "title": room_name.replace("_", " ").title(),
            "description": f"Beschreibung für {room_name}",
            "background_color": [50, 50, 50],
            "entities": [],
            "exits": {},
            "items": []
        }
        
        file_path = f"{self.room_directory}{room_name}.json"
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                json.dump(template, file, indent=2)
            print(f"Raum-Vorlage erstellt: {file_path}")
            return True
        else:
            print(f"Raum '{room_name}' existiert bereits!")
            return False
