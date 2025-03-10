from PyQt6.QtCore import QRect
from typing import Dict, Optional
from CORE.Entities.strategies.Strategy import Strategy

class StrategyManager:
    def __init__(self):
        self._strategies: Dict[int, Strategy] = {}
        self._id_counter = 0

    def _generate_id(self) -> int:
        """Erzeugt eine eindeutige ID für eine neue Strategy."""
        self._id_counter += 1
        return self._id_counter

    def create_strategy(self, name: str, description: str, rect: QRect) -> Strategy:
        """
        Erzeugt ein neues Strategy-Objekt (Factory-Methode), weist ihm eine eindeutige ID zu
        und speichert es im Manager.
        """
        new_id = self._generate_id()
        strategy = Strategy(new_id, name, description)
        strategy.rect = rect
        self._strategies[new_id] = strategy
        return strategy

    def get_strategy(self, ibj_id: int) -> Optional[Strategy]:
        """Gibt das Strategy-Objekt anhand der ID zurück, falls vorhanden."""
        return self._strategies.get(ibj_id)

    def list_strategies(self):
        """Gibt alle im Manager gespeicherten Strategy-Objekte als Liste zurück."""
        return list(self._strategies.values())

    def update_strategy(self, updated_strategy: Strategy) -> bool:
        """
        Aktualisiert ein bestehendes Strategy-Objekt anhand seiner ID.
        Gibt True zurück, wenn die Aktualisierung erfolgreich war.
        """
        existing = self._strategies.get(updated_strategy.ibj_id)
        if existing:
            existing.name = updated_strategy.name
            existing.description = updated_strategy.description
            existing.rect = updated_strategy.rect
            return True
        return False

    def clear(self):
        """Entfernt alle Strategy-Objekte aus dem Manager."""
        self._strategies.clear()
