from typing import List, Union
from PyQt6.QtWidgets import QGraphicsPathItem
from PyQt6.QtGui import QPainter, QPen, QPolygonF, QColor, QPainterPath
from PyQt6.QtCore import QPointF, Qt
from B_CORE.Entities.objectives.Objective import ObjectiveItem
from B_CORE.Entities.strategies.Strategy import StrategyItem
from B_CORE.Entities.measures.Measure import MeasureItem


import math

class CombineRelShip:
    def __init__(
        self,
        rel_id: int,
        name: str,
        description: str,
        source: Union["ObjectiveItem", "StrategyItem"],
        targets: List[Union["StrategyItem", "MeasureItem"]]
    ):
        """
        Generalisierte Klasse für Beziehungen zwischen verschiedenen Entitäten.

        :param rel_id: ID der Beziehung
        :param name: Name der Beziehung
        :param description: Beschreibung der Beziehung
        :param source: Quelle der Beziehung (z.B. ObjectiveItem oder StrategyItem)
        :param targets: Liste der Ziele (z.B. StrategyItem oder MeasureItem)
        """
        self.id = rel_id
        self.name = name
        self.description = description
        self.source = source
        self.targets = targets

    def update_source(self, new_source):
        """Dynamisches Aktualisieren der Quelle."""
        self.source = new_source

    def update_targets(self, new_targets):
        """Dynamisches Aktualisieren der Ziele."""
        self.targets = new_targets

    def __repr__(self):
        return (
            f"CombineRelShip(id={self.id}, name='{self.name}', description='{self.description}', "
            f"source={self.source}, targets={self.targets})"
        )

class CombineRelShipItem(QGraphicsPathItem):
    def __init__(self, rel_id, name, description, source, target):
        super().__init__()
        self.rel_id = rel_id
        self.name = name
        self.description = description
        self.source = source
        self.target = target
        self.setZValue(1)  # Zeichne über anderen Elementen

        # Weiße Linie mit rechteckigen Ecken
        self.setPen(QPen(QColor(255, 255, 255), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap, Qt.PenJoinStyle.MiterJoin))

        self.update_position()

    def update_source(self, new_source):
        """Dynamische Aktualisierung der Quelle."""
        self.source = new_source
        self.update_position()

    def update_target(self, new_target):
        """Dynamische Aktualisierung des Ziels."""
        self.target = new_target
        self.update_position()

    def update_position(self):
        """Berechnet und zeichnet die rechteckige Pfeil-Verbindung neu."""
        if not self.source or not self.target:
            return

        start_point = QPointF(
            self.source.sceneBoundingRect().center().x(),
            self.source.sceneBoundingRect().bottom()
        )

        end_rect = self.target.sceneBoundingRect()
        end_point = QPointF(end_rect.center().x(), end_rect.top() - 1)

        path = QPainterPath()
        path.moveTo(start_point)

        mid_x = start_point.x()
        mid_y = (start_point.y() + end_point.y()) / 2
        path.lineTo(mid_x, mid_y)
        path.lineTo(end_point.x(), mid_y)
        path.lineTo(end_point)

        self.setPath(path)
        self.update_arrow_head(end_point)

    def update_arrow_head(self, end_point):
        """Zeichnet eine sichtbare Pfeilspitze oberhalb des Ziels."""
        arrow_size = 10
        angle = math.pi * 1.5  # Pfeil zeigt nach unten

        p1 = end_point + QPointF(math.cos(angle + math.pi / 6) * arrow_size,
                                 math.sin(angle + math.pi / 6) * arrow_size)
        p2 = end_point + QPointF(math.cos(angle - math.pi / 6) * arrow_size,
                                 math.sin(angle - math.pi / 6) * arrow_size)

        self.arrow_head = QPolygonF([end_point, p1, p2])

    def paint(self, painter: QPainter, option, widget=None):
        """Zeichnet den Pfeil."""
        painter.setPen(self.pen())
        painter.drawPath(self.path())

        painter.setBrush(QColor(255, 255, 255))
        painter.drawPolygon(self.arrow_head)
