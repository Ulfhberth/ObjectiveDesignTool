from typing import Dict, Optional, List
from B_CORE.Entities.objectives.Objective import ObjectiveItem


class ObjectiveManager:
    def __init__(self):
        self._objectives: Dict[int, ObjectiveItem] = {}
        self._id_counter = 0

    def _generate_id(self) -> int:
        self._id_counter += 1
        
        return self._id_counter

    def create_objective(self, name: str, description: str, width: float, height: float) -> ObjectiveItem:
        obj_id = self._generate_id()
        objective = ObjectiveItem(obj_id, name, description, width, height)
        self._objectives[obj_id] = objective
        return objective

    def get_objective(self, obj_id: int) -> Optional[ObjectiveItem]:
        return self._objectives.get(obj_id)

    def list_objectives(self) -> List[ObjectiveItem]:
        return list(self._objectives.values())

    def is_empty(self) -> bool:
        return not self._objectives

    def update_objective(self, updated_objective: ObjectiveItem) -> bool:
        if not isinstance(updated_objective, ObjectiveItem):
            print("Fehler: Ungültiges Objective-Objekt übergeben.")
            return False

        existing_objective = self._objectives.get(updated_objective.objective.id)
        if existing_objective:
            existing_objective.objective.name = updated_objective.objective.name
            existing_objective.objective.description = updated_objective.objective.description
            existing_objective.prepareGeometryChange()
            existing_objective.setRect(updated_objective.rect)
            existing_objective.update()
            return True
        
        print(f"Fehler: Kein Objective mit ID {updated_objective.objective.id} gefunden.")
        return False

    def clear(self):
        self._objectives.clear()
