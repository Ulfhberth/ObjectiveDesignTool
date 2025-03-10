from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtGui import QPainter, QFont, QBrush, QPen, QColor
from PyQt6.QtCore import QRect, Qt
from typing import Optional

class Objective():
    def __init__(self, obj_id: int, name: str, description: str):
        self.id = obj_id
        self.name = name
        self.description = description
        self.rect: Optional[QRect] = None  # QRect wird später gesetzt

    def set_rect(self, x: int, y: int, width: int, height: int):
        """Setzt das QRect des Objectives."""
        self.rect = QRect(x, y, width, height)

    def __repr__(self):
        return (f"Objective(id={self.id}, name='{self.name}', description='{self.description}', "
                f"rect={self.rect})")

