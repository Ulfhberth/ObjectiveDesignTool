from typing import Dict, Optional, List
from B_CORE.Entities.strategies.Strategy import StrategyItem


class StrategyManager:
    def __init__(self):
        self._strategies: Dict[int, StrategyItem] = {}
        self._id_counter = 0

    def _generate_id(self) -> int:
        self._id_counter += 1
        return self._id_counter

    def create_strategy(self, name: str, description: str, width: float, height: float) -> StrategyItem:
        strategy_id = self._generate_id()
        strategy = StrategyItem(strategy_id, name, description, width, height)
        self._strategies[strategy_id] = strategy
        return strategy

    def get_strategy(self, strategy_id: int) -> Optional[StrategyItem]:
        return self._strategies.get(strategy_id)

    def list_strategies(self) -> List[StrategyItem]:
        return list(self._strategies.values())

    def update_strategy(self, updated_strategy: StrategyItem) -> bool:
        if not isinstance(updated_strategy, StrategyItem):
            print("Fehler: Ungültiges Strategy-Objekt übergeben.")
            return False

        existing_strategy = self._strategies.get(updated_strategy.strategy.id)
        if existing_strategy:
            existing_strategy.strategy.name = updated_strategy.strategy.name
            existing_strategy.strategy.description = updated_strategy.strategy.description
            existing_strategy.prepareGeometryChange()
            existing_strategy.setRect(updated_strategy.rect)
            existing_strategy.update()
            return True
        
        print(f"Fehler: Keine Strategy mit ID {updated_strategy.strategy.id} gefunden.")
        return False

    def clear(self):
        self._strategies.clear()
