from typing import List
from B_CORE.Entities.objectives.Objective import ObjectiveItem
from B_CORE.Entities.strategies.Strategy import StrategyItem
from PyQt6.QtWidgets import QGraphicsPathItem
from PyQt6.QtGui import QPainter, QPen, QPolygonF, QColor, QPainterPath
from PyQt6.QtCore import QLineF, QPointF, Qt
import math

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

class CombineRelShipItem(QGraphicsPathItem):
    def __init__(self, rel_id, name, description, sourceobjective, targetstrategy):
        super().__init__()
        self.rel_id = rel_id
        self.name = name
        self.description = description
        self.sourceobjective = sourceobjective  # Startpunkt (ObjectiveItem)
        self.targetstrategy = targetstrategy  # Endpunkt (StrategyItem)
        self.setZValue(1)  # Zeichne über anderen Elementen

        # Weiße Linie mit rechteckigen Ecken
        self.setPen(QPen(QColor(255, 255, 255), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap, Qt.PenJoinStyle.MiterJoin))

        self.update_position()

    def update_position(self):
        """Berechnet und zeichnet die rechteckige Pfeil-Verbindung neu."""
        start_point = QPointF(
        self.sourceobjective.sceneBoundingRect().center().x(),  # X-Koordinate bleibt in der Mitte
        self.sourceobjective.sceneBoundingRect().bottom()       # Y-Koordinate wird auf den unteren Rand gesetzt
        )

        # **Endpunkt leicht über dem oberen Rand des StrategyItem (damit Pfeil sichtbar bleibt)**
        end_rect = self.targetstrategy.sceneBoundingRect()
        end_point = QPointF(end_rect.center().x(), end_rect.top() - 1)  # 5 Pixel über der oberen Grenze

        path = QPainterPath()
        path.moveTo(start_point)

        # **Rechteckige Linienführung**
        mid_x = start_point.x()
        mid_y = (start_point.y() + end_point.y()) / 2  # Mittelpunkt vertikal
        path.lineTo(mid_x, mid_y)  # Senkrecht nach unten
        path.lineTo(end_point.x(), mid_y)  # Horizontal zum Zielpunkt
        path.lineTo(end_point)  # Senkrecht zum oberen Rand des StrategyItem (leicht darüber)

        self.setPath(path)

        # **Pfeilspitze berechnen**
        self.update_arrow_head(end_point)

    def update_arrow_head(self, end_point):
        """Zeichnet eine sichtbare Pfeilspitze oberhalb des StrategyItems."""
        arrow_size = 10 
        angle = math.pi*1.5   # Pfeil zeigt immer nach unten

        p1 = end_point + QPointF(math.cos(angle + math.pi / 6) * arrow_size,
                                 math.sin(angle + math.pi / 6) * arrow_size)
        p2 = end_point + QPointF(math.cos(angle - math.pi / 6) * arrow_size,
                                 math.sin(angle - math.pi / 6) * arrow_size)

        self.arrow_head = QPolygonF([end_point, p1, p2])

    def paint(self, painter: QPainter, option, widget=None):
        """Zeichnet den Pfeil."""
        painter.setPen(self.pen())
        painter.drawPath(self.path())

        painter.setBrush(QColor(255, 255, 255))  # Weiße Pfeilspitze
        painter.drawPolygon(self.arrow_head)
