from PyQt6.QtCore import QRect
from typing import Dict, Optional
from CORE.Entities.objectives.Objective import Objective


class ObjectiveManager:
    def __init__(self):
        self._objectives: Dict[int, Objective] = {}
        self._id_counter = 0
    
    def _generate_id(self) -> int:
        """Erzeugt eine eindeutige ID für ein neues Objective."""
        self._id_counter += 1
        return self._id_counter
    
    def create_objective(self, name: str, description: str, rect: QRect) -> Objective:
        """erzeugt ein neues Objective in der Liste"""
        obj_id = self._generate_id()
        objective = Objective(obj_id, name, description)
        self._objectives[obj_id] = objective
        objective.rect = rect
        return objective
    
    def get_objective(self, obj_id: int) -> Optional[Objective]:
        """Gibt ein Objective anhand seiner ID zurück."""
        return self._objectives.get(obj_id, None)
    
    def list_objectives(self):
        """Gibt alle erstellten Objectives zurück."""
        return list(self._objectives.values())

    def is_empty(self) -> bool:
        """Gibt True zurück, wenn keine Objectives existieren."""
        return len(self._objectives) == 0
    
    def update_objective(self, updated_objective: Objective) -> bool:
        """Ersetzt ein bestehendes Objective durch eine aktualisierte Version."""
    
        if updated_objective is None:
            print("Fehler: Das übergebene Objective ist None.")
            return False

        if not isinstance(updated_objective, Objective):
            print("Fehler: Das übergebene Objekt ist keine gültige Objective-Instanz.")
            return False

        existing_objective = self._objectives.get(updated_objective.id)
        if existing_objective:
            # Nur Werte aktualisieren, statt die ganze Instanz zu ersetzen
            existing_objective.name = updated_objective.name
            existing_objective.description = updated_objective.description
            existing_objective.rect = updated_objective.rect
            return True
        else:
            print(f"Fehler: Kein Objective mit ID {updated_objective.id} gefunden.")
            return False
