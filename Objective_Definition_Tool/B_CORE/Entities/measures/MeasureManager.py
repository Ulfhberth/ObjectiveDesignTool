from typing import Dict, Optional, List
from CORE.Entities.measures.Measure import MeasureItem


class MeasureManager:
    def __init__(self):
        self._measures: Dict[int, MeasureItem] = {}
        self._id_counter = 0

    def _generate_id(self) -> int:
        """Erzeugt eine eindeutige ID für ein neues Measure."""
        self._id_counter += 1
        return self._id_counter

    def create_measure(self, name: str, description: str, width: float, height: float) -> MeasureItem:
        """Erzeugt ein neues Measure und fügt es der Liste hinzu."""
        measure_id = self._generate_id()
        measure_item = MeasureItem(measure_id, name, description, width, height)
        self._measures[measure_id] = measure_item
        return measure_item

    def get_measure(self, measure_id: int) -> Optional[MeasureItem]:
        """Gibt ein MeasureItem anhand seiner ID zurück."""
        return self._measures.get(measure_id, None)

    def list_measures(self) -> List[MeasureItem]:
        """Gibt alle erstellten Measures zurück."""
        return list(self._measures.values())

    def is_empty(self) -> bool:
        """Gibt True zurück, wenn keine Measures existieren."""
        return len(self._measures) == 0

    def update_measure(self, updated_measure: MeasureItem) -> bool:
        """Aktualisiert ein bestehendes MeasureItem."""
        existing_measure = self._measures.get(updated_measure.measure.id)
        if existing_measure:
            existing_measure.measure.name = updated_measure.measure.name
            existing_measure.measure.description = updated_measure.measure.description
            existing_measure.prepareGeometryChange()
            existing_measure.setRect(updated_measure.rect)
            existing_measure.update()
            return True
        else:
            print(f"Fehler: Kein Measure mit ID {updated_measure.measure.id} gefunden.")
            return False
