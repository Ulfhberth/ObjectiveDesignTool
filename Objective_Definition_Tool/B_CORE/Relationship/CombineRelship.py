from typing import List
from B_CORE.Entities.objectives.Objective import ObjectiveItem
from B_CORE.Entities.strategies.Strategy import StrategyItem


class CombineRelShip:
    def __init__(
        self,
        rel_id: int,
        name: str,
        description: str,
        sourceobjective: ObjectiveItem,
        targetstrategies: List[StrategyItem]
    ):
        self.id = rel_id
        self.name = name
        self.description = description
        self.sourceobjective = sourceobjective
        self.targetstrategies = targetstrategies

    def __repr__(self):
        return (
            f"CombineRelShip(id={self.id}, name='{self.name}', description='{self.description}', "
            f"sourceobjective={self.sourceobjective}, targetstrategies={self.targetstrategies})"
        )
