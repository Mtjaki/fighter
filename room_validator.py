#!/usr/bin/env python3
"""
Raum-Validierungs- und Verwaltungsskript für das Fighter-Spiel
"""

import sys
import os
sys.path.append('src')

from room_manager import RoomManager

def main():
    print("=== Fighter Raum-Manager ===\n")
    
    room_manager = RoomManager()
    
    # Verfügbare Räume auflisten
    print("Verfügbare Räume:")
    for room in room_manager.list_available_rooms():
        info = room_manager.get_room_info(room)
        if info:
            print(f"  - {room}: {info['title']}")
            print(f"    Entitäten: {info['entity_count']}, Ausgänge: {', '.join(info['exits']) if info['exits'] else 'Keine'}")
        else:
            print(f"  - {room}: (Fehler beim Laden)")
    
    print("\n" + "="*50)
    
    # Validierung der Raumverbindungen
    print("\nValidiere Raumverbindungen...")
    issues = room_manager.validate_room_connections()
    
    if issues:
        print("⚠️  Probleme gefunden:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ Alle Raumverbindungen sind gültig!")
    
    print("\n" + "="*50)
    
    # Interaktives Menü
    while True:
        print("\nOptionen:")
        print("1. Raum-Details anzeigen")
        print("2. Neuen Raum erstellen")
        print("3. Raum-Karte anzeigen")
        print("4. Beenden")
        
        choice = input("\nWähle eine Option (1-4): ").strip()
        
        if choice == "1":
            room_name = input("Raumname: ").strip()
            info = room_manager.get_room_info(room_name)
            if info:
                print(f"\n--- {info['title']} ---")
                print(f"Beschreibung: {info['description']}")
                print(f"Entitäten: {info['entity_count']}")
                print(f"Ausgänge: {', '.join(info['exits']) if info['exits'] else 'Keine'}")
            else:
                print("Raum nicht gefunden!")
                
        elif choice == "2":
            room_name = input("Name des neuen Raums: ").strip()
            if room_manager.create_room_template(room_name):
                print(f"Raum '{room_name}' erfolgreich erstellt!")
            
        elif choice == "3":
            print("\n--- Raum-Karte ---")
            show_room_map(room_manager)
            
        elif choice == "4":
            break
        else:
            print("Ungültige Auswahl!")

def show_room_map(room_manager):
    """Zeigt eine einfache ASCII-Karte der Raumverbindungen"""
    rooms = room_manager.list_available_rooms()
    
    print("\nRaumverbindungen:")
    for room in rooms:
        info = room_manager.get_room_info(room)
        if info and info['exits']:
            print(f"\n{room}:")
            # Lade die tatsächlichen Exit-Daten aus der JSON
            try:
                import json
                with open(f"src/rooms/{room}.json", "r") as file:
                    data = json.load(file)
                    exits = data.get('exits', {})
                    for direction, target in exits.items():
                        print(f"  {direction} → {target}")
            except:
                print(f"  (Fehler beim Laden der Exits für {room})")

if __name__ == "__main__":
    main()
