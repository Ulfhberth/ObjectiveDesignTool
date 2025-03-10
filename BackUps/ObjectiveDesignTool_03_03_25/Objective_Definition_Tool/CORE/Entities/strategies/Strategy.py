from PyQt6.QtCore import QRect
from typing import Optional

class Strategy:
    def __init__(self, ibj_id: int, name: str, description: str):
        self.ibj_id = ibj_id
        self.name = name
        self.description = description
        self.rect: Optional[QRect] = None  # Das Rechteck wird später gesetzt

    def set_rect(self, x: int, y: int, width: int, height: int):
        """Setzt das QRect der Strategy."""
        self.rect = QRect(x, y, width, height)

    def __repr__(self):
        return (f"Strategy(ibj_id={self.ibj_id}, name='{self.name}', "
                f"description='{self.description}', rect={self.rect})")