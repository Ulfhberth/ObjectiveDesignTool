from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtGui import QPainter, QFont, QBrush, QPen, QColor, QFontMetrics
from PyQt6.QtCore import QRectF, Qt


class Measure():
    def __init__(self, measure_id: int, name: str, description: str):
        self.id = measure_id
        self.name = name
        self.description = description

    def __repr__(self):
        return (f"Measure(id={self.id}, name='{self.name}', description='{self.description}')")


class MeasureItem(QGraphicsItem):
    def __init__(self, measure_id, name, description, width, height):
        super().__init__()
        self.measure = Measure(measure_id, name, description)
        self.rect = QRectF(0, 0, width, height)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setAcceptedMouseButtons(Qt.MouseButton.RightButton)

    def boundingRect(self) -> QRectF:
        return self.rect

    def paint(self, painter: QPainter, option, widget=None):
        font = QFont("Arial", 12)
        painter.setFont(font)
        font_metrics = painter.fontMetrics()
        name_wrapped = self.wrap_text(self.measure.name, self.rect.width() - 20, font_metrics)
        description_wrapped = self.wrap_text(self.measure.description, self.rect.width() - 20, font_metrics)
        combined_text = name_wrapped + "\n" + description_wrapped

        if self.isSelected():
            painter.setBrush(QBrush(QColor(0, 255, 0, 100)))  # Grün, wenn ausgewählt
            painter.setPen(QPen(Qt.GlobalColor.green, 3))
        else:
            painter.setBrush(QBrush(QColor(180, 180, 180)))
            painter.setPen(QPen(Qt.GlobalColor.black, 1))

        painter.drawRect(self.rect)
        text_x = self.rect.x() + 10
        text_y = self.rect.y() + font_metrics.height()
        for line in combined_text.split("\n"):
            painter.drawText(int(text_x), int(text_y), line)
            text_y += font_metrics.height()

    def wrap_text(self, text, max_width, font_metrics: QFontMetrics):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if font_metrics.horizontalAdvance(current_line + word) <= max_width:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return "\n".join(lines)
