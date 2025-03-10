### gui.py
import sys
import os
from PyQt6.QtWidgets import QMenu, QDialog, QGraphicsView, QGraphicsScene, QMenu
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QAction, QPolygonF 
from PyQt6.QtCore import Qt, QRect, QPointF, QRectF 
from App_GUI.dialogs.EditObjectiveDialog import EditObjectiveDialog
from App_GUI.dialogs.NewObjectiveDialog import NewObjectiveDialog
from App_GUI.dialogs.NewStrategyDialog import NewStrategyDialog
from CORE.Entities.objectives.ObjectiveManager import ObjectiveManager
from CORE.Entities.strategies.StrategyManager import StrategyManager
import math

class Canvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.rectangles = []  # Speichert Rechtecke und zugehörige Namen/Beschreibungen
        self.objective_manager = ObjectiveManager()
        self.strategy_manager = StrategyManager()  # Neuer Manager für Strategy-Objekte
        self.selected_rect = None
        self.drawing = False
        self.start_point = QPointF()
        self.current_rect = QRectF()

    # --------------------------------------------------
    # ------- alle Mausrelevanten Methoden -------------
    # --------------------------------------------------
    
    def mousePressEvent(self, event): 
        print("Button clicked")
        print(f"Klick-Position: {event.pos()}")

        if event.button() == Qt.MouseButton.LeftButton:
            print("Left Mouse Button Clicked")
            # deselect a chosen rectangle
            self.selected_rect = None
            
            self.drawing = True
            self.start_point = self.mapToScene(event.pos())
            self.current_rect = QRectF(self.start_point, self.start_point)
            self.viewport().update()

        elif event.button() == Qt.MouseButton.RightButton:
            print("Right Mouse Button Clicked")
            view_click_position = event.pos()
            scene_click_position = self.mapToScene(view_click_position)
            
            if self.objective_manager.is_empty():
                print("Empty Context Menu Shown")
                self.showEmptyContextMenu(view_click_position)
                self.selected_rect = None
                return

            found_objective = None
            for obj in self.objective_manager.list_objectives():
                # Konvertiere scene_click_position in QPoint
                if obj.rect.contains(scene_click_position.toPoint()):
                    found_objective = obj
                    break

            if found_objective:
                print(f"Objective gefunden: {found_objective}")
                self.selected_rect = found_objective
                self.showRectangleContextMenu(view_click_position)
            else:
                print("Kein Objective gefunden, Standard-Menü wird angezeigt")
                self.showEmptyContextMenu(view_click_position)
        
        self.viewport().update()

    def mouseMoveEvent(self, event):
        if self.drawing:
            end_point = self.mapToScene(event.pos())
            self.current_rect = QRectF(self.start_point, end_point).normalized()
            self.viewport().update()    

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            self.current_rect = QRectF()  # Reset des Rechtecks
            self.viewport().update()      
    
    # --------------------------------------------------
    # ------------ Menü-Aufruf Methoden ----------------
    # --------------------------------------------------
        
    def showEmptyContextMenu(self, position):
        context_menu = QMenu(self)
        
        # Aktion zum Hinzufügen eines neuen Objectives
        new_objective_action = QAction("New Objective...", self)
        new_objective_action.triggered.connect(lambda: self.openObjectiveDialog(position))
        context_menu.addAction(new_objective_action)
        
        # Falls mindestens ein Objective existiert, kann auch eine Strategy hinzugefügt werden
        if not self.objective_manager.is_empty():
            new_strategy_action = QAction("New Strategy...", self)
            new_strategy_action.triggered.connect(lambda: self.NewStrategyDialog(position))
            context_menu.addAction(new_strategy_action)
        
        context_menu.exec(self.mapToGlobal(position))

    def open_edit_dialog(self):
        # Hier wird davon ausgegangen, dass self.selected_rect nun das ausgewählte Objective (und nicht nur sein QRect) ist.
        if self.selected_rect:
            dialog = EditObjectiveDialog(self.selected_rect, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                updated_objective = dialog.get_updated_objective()
                self.objective_manager.update_objective(updated_objective)
                self.viewport().update()

    def showRectangleContextMenu(self, position):
        context_menu = QMenu(self)
        edit_objective_action = QAction("Edit Objective", self)
        edit_objective_action.triggered.connect(self.open_edit_dialog)
        context_menu.addAction(edit_objective_action)

        context_menu.exec(self.mapToGlobal(position))

    def openObjectiveDialog(self, position):
        # Bestehende Methode zum Hinzufügen von Objectives
        dialog = NewObjectiveDialog("new objective", "", self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            objective_name, objective_desc = dialog.get_new_values()
            # Position in Szenenkoordinaten umrechnen
            scene_pos = self.mapToScene(position)
            newrect = QRect(int(scene_pos.x()), int(scene_pos.y()), 10, 10)
            newobj = self.objective_manager.create_objective(objective_name, objective_desc, newrect)
            print(newobj)
            self.viewport().update()

    def NewStrategyDialog(self, position):
        """
        Fügt ein neues Strategy-Objekt als Rechteck zum Canvas hinzu.
        Es wird geprüft, ob mindestens ein Objective existiert. Falls nicht, wird die Erzeugung
        eines Strategy-Objekts verhindert.
        """
        # Einschränkung: Strategies dürfen erst hinzugefügt werden, wenn mindestens ein Objective existiert
        if self.objective_manager.is_empty():
            print("Es muss mindestens ein Objective vorhanden sein, um eine Strategy hinzuzufügen.")
            return

        print("neue Strategy dialog")
        dialog = NewStrategyDialog("new strategy", "", self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            strategy_name, strategy_desc = dialog.get_new_values()
            # Umrechnung von View- zu Scene-Koordinaten
            scene_pos = self.mapToScene(position)
            new_rect = QRect(int(scene_pos.x()), int(scene_pos.y()), 10, 10)
            new_strategy = self.strategy_manager.create_strategy(strategy_name, strategy_desc, new_rect)
            print(new_strategy)
            self.viewport().update()

    # --------------------------------------------------
    # ------------ Canvas-Mal-FUnktion -----------------
    # --------------------------------------------------
    
    def wrap_text(self, text, max_width, font_metrics):
        """Bricht den Text um, sodass er innerhalb der gegebenen Breite bleibt."""
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font_metrics.horizontalAdvance(test_line) > max_width:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)
        return "\n".join(lines)

    def drawForeground(self, painter: QPainter, rect: 'QRectF'):
    
        # Initialisierung der relevanten Funktionen
        print("drawForeground wird aufgerufen")
        font = QFont("Arial", 12)
        painter.setFont(font)
        font_metrics = painter.fontMetrics()
        self.rectangles.clear()

        # maximale Breite der Textboxen 
        max_width = 500
        
        # Ermittelt das sichtbare Szenenrechteck anhand des aktuellen Viewports
        
        # identifiziere das aktuell sichtbare Rechteck der Szene basierend auf dem Viewport
        scene_rect = self.mapToScene(self.viewport().rect()).boundingRect()
        
        # berechnen die zentrale x-Koordinate und eine y-Koordinate
        center_x = scene_rect.center().x()
        
        # 10 Pixel vom oberen Rand der sichtbaren Szene
        top_y = scene_rect.top() + 10  

        # Wenn self.drawing wahr ist, wird ein gestricheltes rotes Rechteck (self.current_rect) gezeichnet.
        if self.drawing:
            painter.setPen(QPen(Qt.GlobalColor.red, 2, Qt.PenStyle.DashLine))
            painter.drawRect(self.current_rect)
        
        # --------------------------------------------------
        # ----- Zeichnen der Objectives auf dem Canvas -----
        # --------------------------------------------------
        
        # Die Funktion self.objective_manager.list_objectives() liefert eine Liste von Objectives.
        objectives = self.objective_manager.list_objectives()
        
        for objective in objectives:
            
            # Für jedes Objective werden der Name und die Beschreibung umbrochen, um die Textbreite zu begrenzen.
            name_wrapped = self.wrap_text(objective.name, max_width - 20, font_metrics)
            description_wrapped = self.wrap_text(objective.description, max_width - 20, font_metrics)
            combined_text = name_wrapped + "\n" + description_wrapped

            text_width = max(font_metrics.horizontalAdvance(line) for line in combined_text.split("\n")) + 20
            text_height = font_metrics.height() * (combined_text.count("\n") + 1) + 20

            rect_width = min(max(200, text_width), max_width)
            rect_height = max(100, text_height)

            objective.rect.setWidth(rect_width)
            objective.rect.setHeight(rect_height)
            
            # Zentriere das Objective horizontal und positioniere 10 Pixel vom oberen Rand
            new_x = int(center_x - rect_width / 2)
            objective.rect.moveTo(new_x, int(top_y))

            self.rectangles.append((objective.rect, objective.name, objective.description))

            # Das Rechteck wird gezeichnet, wobei ein roter Rahmen verwendet wird, wenn das Objective ausgewählt ist, andernfalls ein schwarzer.
            if self.selected_rect and hasattr(self.selected_rect, "id") and self.selected_rect.id == objective.id:
                painter.setBrush(QBrush(QColor(255, 0, 0, 100)))  # Rot, wenn ausgewählt
                painter.setPen(QPen(Qt.GlobalColor.red, 3))
            else:
                painter.setBrush(QBrush(QColor(200, 200, 200)))
                painter.setPen(QPen(Qt.GlobalColor.black, 1))


            painter.drawRect(objective.rect)
            font.setUnderline(True)
            painter.setFont(font)
            text_x = objective.rect.x() + 10
            text_y = objective.rect.y() + font_metrics.height()
            for line in combined_text.split("\n"):
                painter.drawText(text_x, text_y, line)
                text_y += font_metrics.height()
        # --------------------------------------------------
        # -----  Zeichne Strategies auf dem Canvas ---------
        # --------------------------------------------------

        # Die Strategies werden nebeneinander mit einem Abstand von 50 Pixeln angeordnet.
        strategies = self.strategy_manager.list_strategies()
        if strategies:
            strategy_offset = 250  # vertikaler Versatz: Strategies werden unterhalb der Objectives platziert
            dimensions = []  # Speichert (strategy, rect_width, rect_height, combined_text)
            for strategy in strategies:
                name_wrapped = self.wrap_text(strategy.name, max_width - 20, font_metrics)
                description_wrapped = self.wrap_text(strategy.description, max_width - 20, font_metrics)
                combined_text = name_wrapped + "\n" + description_wrapped

                text_width = max(font_metrics.horizontalAdvance(line) for line in combined_text.split("\n")) + 20
                text_height = font_metrics.height() * (combined_text.count("\n") + 1) + 20

                rect_width = min(max(200, text_width), max_width)
                rect_height = max(100, text_height)

                strategy.rect.setWidth(rect_width)
                strategy.rect.setHeight(rect_height)
                dimensions.append((strategy, rect_width, rect_height, combined_text))

            # Gesamtbreite aller Strategies inklusive 50 Pixel Abstand zwischen den einzelnen
            total_width = sum(item[1] for item in dimensions) + (len(dimensions) - 1) * 50
            start_x = int(center_x - total_width / 2)

            # Für jeden Strategy wird das Rechteck positioniert und anschließend ein Pfeil gezeichnet.
            for strategy, rect_width, rect_height, combined_text in dimensions:
                # Positioniere Strategy-Rechteck
                strategy.rect.moveTo(start_x, int(top_y + strategy_offset))
                painter.setBrush(QBrush(QColor(0, 0, 255, 100)))  # Halbtransparentes Blau
                painter.setPen(QPen(Qt.GlobalColor.blue, 3))
                painter.drawRect(strategy.rect)

                # Zeichne den Text in der Strategy
                font.setUnderline(True)
                painter.setFont(font)
                text_x = strategy.rect.x() + 10
                text_y = strategy.rect.y() + font_metrics.height()
                for line in combined_text.split("\n"):
                    painter.drawText(text_x, text_y, line)
                    text_y += font_metrics.height()

                # ----------------------------------------------------------------------
                # -----  Zeichnen der Pfeile zwischen Strategys auf dem Canvas ---------
                # ----------------------------------------------------------------------

                # Zeichne einen Pfeil vom (ersten) Objective zur Strategy
                if objectives:
                    # Verwende als Ausgangspunkt das untere Zentrum des ersten Objectives
                    source = objectives[0]
                    start_point = QPointF(source.rect.x() + source.rect.width() / 2,
                                        source.rect.y() + source.rect.height())
                    # Zielpunkt: oberes Zentrum der Strategy
                    end_point = QPointF(strategy.rect.x() + strategy.rect.width() / 2,
                                        strategy.rect.y())
                    # Zeichne die Linie
                    painter.setPen(QPen(Qt.GlobalColor.white, 2))
                    painter.drawLine(start_point, end_point)

                    # Berechne die Pfeilspitze
                    dx = end_point.x() - start_point.x()
                    dy = end_point.y() - start_point.y()
                    angle = math.atan2(dy, dx)
                    arrow_size = 10
                    arrow_angle = math.radians(30)
                    point1 = QPointF(
                        end_point.x() - arrow_size * math.cos(angle - arrow_angle),
                        end_point.y() - arrow_size * math.sin(angle - arrow_angle)
                    )
                    point2 = QPointF(
                        end_point.x() - arrow_size * math.cos(angle + arrow_angle),
                        end_point.y() - arrow_size * math.sin(angle + arrow_angle)
                    )
                    arrow_head = QPolygonF([end_point, point1, point2])
                    painter.setBrush(QBrush(Qt.GlobalColor.black))
                    painter.drawPolygon(arrow_head)

                start_x += rect_width + 50  # Erhöhe x um Rechtecksbreite + 50 Pixel Abstand
       