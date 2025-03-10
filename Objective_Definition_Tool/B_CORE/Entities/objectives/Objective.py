from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtGui import QPainter, QFont, QBrush, QPen, QColor
from PyQt6.QtCore import QRectF, Qt


class Objective:
    def __init__(self, obj_id: int, name: str, description: str):
        self.id = obj_id
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Objective(id={self.id}, name='{self.name}', description='{self.description}')"


class ObjectiveItem(QGraphicsItem):
    def __init__(self, obj_id, name, description, width, height):
        super().__init__()
        self.objective = Objective(obj_id, name, description)
        self.rect = QRectF(0, 0, width, height)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
                      QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

    def boundingRect(self) -> QRectF:
        return self.rect

    def paint(self, painter: QPainter, option, widget=None):
        self.draw_objective(painter)

    def draw_objective(self, painter: QPainter):
        font = QFont("Arial", 12)
        painter.setFont(font)
        font_metrics = painter.fontMetrics()
        wrapped_text = self.wrap_text(self.objective.name, self.objective.description, self.rect.width() - 20, font_metrics)

        painter.setBrush(QBrush(QColor(255, 0, 0, 100)) if self.isSelected() else QBrush(QColor(200, 200, 200)))
        painter.setPen(QPen(Qt.GlobalColor.red if self.isSelected() else Qt.GlobalColor.black, 3 if self.isSelected() else 1))
        painter.drawRect(self.rect)

        text_x, text_y = self.rect.x() + 10, self.rect.y() + font_metrics.height()
        for line in wrapped_text.split("\n"):
            painter.drawText(int(text_x), int(text_y), line)
            text_y += font_metrics.height()

    def wrap_text(self, name, description, max_width, font_metrics):
        def process_text(text):
            words, lines, current_line = text.split(), [], ""
            for word in words:
                if font_metrics.horizontalAdvance(current_line + word) <= max_width:
                    current_line += word + " "
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                lines.append(current_line.strip())
            return "\n".join(lines)
        
        return f"{process_text(name)}\n{process_text(description)}"
