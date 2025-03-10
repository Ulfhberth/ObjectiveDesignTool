from typing import Dict, Optional, List
from B_CORE.Relationship.CombineRelship import CombineRelShipItem

class RelationshipManager:
    def __init__(self):
        self._relationships: Dict[int, CombineRelShipItem] = {}  # Speichert Beziehungen mit ID
        self._id_counter = 0  # ID-Zähler für neue Beziehungen

    def _generate_id(self) -> int:
        """Erzeugt eine eindeutige ID für eine neue Beziehung."""
        self._id_counter += 1
        return self._id_counter

    def create_combine_relationship(self, name: str, description: str, sourceobjective, targetstrategy) -> CombineRelShipItem:
        """
        Erstellt eine CombineRelShipItem-Verbindung zwischen einem ObjectiveItem und einem StrategyItem.
        """
        rel_id = self._generate_id()
        relationship = CombineRelShipItem(rel_id, name, description, sourceobjective, targetstrategy)
        self._relationships[rel_id] = relationship
        return relationship

    def get_relationship(self, rel_id: int) -> Optional[CombineRelShipItem]:
        """Gibt eine RelationshipItem anhand ihrer ID zurück."""
        return self._relationships.get(rel_id, None)

    def list_relationships(self) -> List[CombineRelShipItem]:
        """Gibt alle gespeicherten RelationshipItem-Objekte als Liste zurück."""
        return list(self._relationships.values())

    def remove_relationship(self, rel_id: int) -> bool:
        """Entfernt eine RelationshipItem anhand ihrer ID."""
        if rel_id in self._relationships:
            del self._relationships[rel_id]
            return True
        return False

    def clear(self):
        """Entfernt alle RelationshipItem-Objekte aus dem Manager."""
        self._relationships.clear()
