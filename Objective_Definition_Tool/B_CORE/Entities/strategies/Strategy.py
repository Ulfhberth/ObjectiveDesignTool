from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtGui import QPainter, QFont, QBrush, QPen, QColor, QFontMetrics


class Strategy:
    def __init__(self, strategy_id: int, name: str, description: str):
        self.id = strategy_id
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Strategy(id={self.id}, name='{self.name}', description='{self.description}')"


class StrategyItem(QGraphicsItem):
    def __init__(self, strategy_id, name, description, width, height, canvas):
        super().__init__()
        self.strategy = Strategy(strategy_id, name, description)
        self.rect = QRectF(0, 0, width, height)
        self.canvas = canvas
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
                      QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

    def boundingRect(self) -> QRectF:
        return self.rect

    def paint(self, painter: QPainter, option, widget=None):
        self.draw_strategy(painter)

    def draw_strategy(self, painter: QPainter):
        font = QFont("Arial", 12)
        painter.setFont(font)
        font_metrics = painter.fontMetrics()
        wrapped_text = self.wrap_text(self.strategy.name, self.strategy.description, self.rect.width() - 20, font_metrics)

        painter.setBrush(QBrush(QColor(0, 0, 255, 100)) if self.isSelected() else QBrush(QColor(220, 220, 220)))
        painter.setPen(QPen(Qt.GlobalColor.blue if self.isSelected() else Qt.GlobalColor.black, 3 if self.isSelected() else 1))
        painter.drawRect(self.rect)

        text_x, text_y = self.rect.x() + 10, self.rect.y() + font_metrics.height()
        for line in wrapped_text.split("\n"):
            painter.drawText(int(text_x), int(text_y), line)
            text_y += font_metrics.height()

    def wrap_text(self, name, description, max_width, font_metrics: QFontMetrics):
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

    def itemChange(self, change, value):
        """Löst `arrange_items()` aus, wenn sich das StrategyItem bewegt."""
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            self.canvas.arrange_items()  # Alle Items und Pfeile neu anordnen
        return super().itemChange(change, value)