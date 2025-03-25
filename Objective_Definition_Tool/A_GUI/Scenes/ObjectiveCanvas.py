from PyQt6.QtWidgets import QMenu, QDialog, QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPainter, QAction, QPen, QColor
from PyQt6.QtCore import Qt, QRectF, QPointF
from A_GUI.Dialogs.NewObjectiveDialog import NewObjectiveDialog
from A_GUI.Dialogs.NewStrategyDialog import NewStrategyDialog
from A_GUI.Dialogs.NewMeasureDialog import NewMeasureDialog
from B_CORE.Entities.objectives.ObjectiveManager import ObjectiveManager
from B_CORE.Entities.strategies.StrategyManager import StrategyManager
from B_CORE.Entities.measures.MeasureManager import MeasureManager
from B_CORE.Relationship.RelShipManager import RelationshipManager

class ObjectiveCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.my_scene = QGraphicsScene(0, 0, 10000, 10000)
        self.setScene(self.my_scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.scale_factor = 1.0
        self.objective_manager = ObjectiveManager()
        self.strategy_manager = StrategyManager()
        self.measure_manager = MeasureManager()
        self.relationship_manager = RelationshipManager()
        self.selected_rect = None
        self.selecting = False
        self.start_point = QPointF()
        self.current_rect = QRectF()
        self.selection_rect = QRectF()

    def clear_relationships(self):
        """Entfernt alle RelationshipItems aus der Szene."""
        for relationship in self.relationship_manager.list_relationships():
            self.my_scene.removeItem(relationship)
        #self.relationship_manager.clear()
    
    def arrange_items(self, spacing_y=50):
        """
        Ordnet die Items gemäß CombineRelShipItems:
        - Objective zentriert oben
        - Strategies darunter basierend auf Objective→Strategy-Relationships
        - Measures darunter zentriert unter der jeweiligen Strategy (horizontal verteilt)
        - Measures kollidieren nicht – globaler Abstand
        - Beziehungen werden entsprechend neu gezeichnet
        """

        objectives = self.objective_manager.list_objectives()
        if not objectives:
            print("Kein Objective vorhanden.")
            return

        # Objective platzieren
        scene_width = self.my_scene.sceneRect().width()
        objective = objectives[0]
        obj_x = (scene_width - objective.boundingRect().width()) / 2
        obj_y = 50
        objective.setPos(obj_x, obj_y)

        # Alle aktuellen Beziehungen holen
        all_relationships = self.relationship_manager.list_relationships()
        print(len(all_relationships))

        # Step 1: Strategies finden, die mit diesem Objective verbunden sind
        strategy_relationships = [
            rel for rel in all_relationships
            if hasattr(rel.source, "objective") and rel.source.objective.id == objective.objective.id
        ]
        strategies = [rel.target for rel in strategy_relationships]

        # Strategies positionieren
        total_width = sum(strategy.boundingRect().width() for strategy in strategies) + (len(strategies) - 1) * 20
        start_x = (scene_width - total_width) / 2
        strat_y = obj_y + objective.boundingRect().height() + spacing_y

        strategy_positions = {}
        x_offset = start_x

        for strategy in strategies:
            strategy.setPos(x_offset, strat_y)
            strategy_positions[strategy.strategy.id] = (
                strategy,
                x_offset,
                strat_y + strategy.boundingRect().height() + spacing_y
            )
            x_offset += strategy.boundingRect().width() + 20

        # Measures zur Szene hinzufügen, falls noch nicht vorhanden
        for rel in all_relationships:
            if hasattr(rel.target, "measure") and rel.target.scene() is None:
                self.my_scene.addItem(rel.target)

        # Globale Liste platzierter Measures
        globally_placed_measures = []

        # Measures unter zugehörigen Strategies zentriert und kollisionsfrei platzieren
        for strategy_id, (strategy, base_x, measure_y) in strategy_positions.items():
            # Alle zugehörigen Measures zur Strategy finden
            measure_relationships = [
                rel for rel in all_relationships
                if hasattr(rel.source, "strategy")
                and rel.source.strategy.id == strategy_id
                and hasattr(rel.target, "measure")
            ]
            measures = [rel.target for rel in measure_relationships]
            if not measures:
                continue

            total_width = sum(m.boundingRect().width() for m in measures) + (len(measures) - 1) * 20
            start_x = strategy.sceneBoundingRect().center().x() - total_width / 2
            x_offset = start_x

            for measure in measures:
                measure.setPos(x_offset, measure_y)

                # Kollisionsprüfung mit allen anderen Measures
                while any(measure.collidesWithItem(other) for other in globally_placed_measures):
                    x_offset += measure.boundingRect().width() + 50
                    measure.setPos(x_offset, measure_y)

                globally_placed_measures.append(measure)
                x_offset += measure.boundingRect().width() + 20

        # Step: Strategies neu zentrieren über ihren Measures
        for strategy_id, (strategy, _, measure_y) in strategy_positions.items():
            related_measures = [
                rel.target for rel in all_relationships
                if hasattr(rel.source, "strategy")
                and rel.source.strategy.id == strategy_id
                and hasattr(rel.target, "measure")
            ]
            if not related_measures:
                continue

            left = min(m.sceneBoundingRect().left() for m in related_measures)
            right = max(m.sceneBoundingRect().right() for m in related_measures)
            center_x = (left + right) / 2
            strategy_x = center_x - strategy.boundingRect().width() / 2

            # Y bleibt gleich
            strategy_y = strategy.scenePos().y()
            strategy.setPos(strategy_x, strategy_y)
        
         # Step: Objective zentrieren über allen Strategies
        if strategies:
            left = min(s.sceneBoundingRect().left() for s in strategies)
            right = max(s.sceneBoundingRect().right() for s in strategies)
            center_x = (left + right) / 2
            objective_x = center_x - objective.boundingRect().width() / 2

            # Y bleibt wie gehabt
            objective_y = objective.scenePos().y()
            objective.setPos(objective_x, objective_y)
        
        # Alle Relationships neu zeichnen
        for rel in all_relationships:
            print(f"starte update for: {rel}")
            rel.update_position()



# --------------------------------------------------------------
# ---------------- mouse related events ------------------------
# --------------------------------------------------------------

    def wheelEvent(self, event):
        zoom_factor = 1.15 if event.angleDelta().y() > 0 else 1 / 1.15
        self.scale(zoom_factor, zoom_factor)
        self.scale_factor *= zoom_factor

    def mousePressEvent(self, event):
        # Konvertiere die Mausposition von View-Koordinaten zu Szenen-Koordinaten
        scene_position = self.mapToScene(event.pos())
        print(f"Mausklick an Szene-Position: {scene_position}")

        if event.button() == Qt.MouseButton.LeftButton:
            print("Linke Maustaste erkannt - Starte Zeichnungsvorgang")
            self.selecting = True
            self.start_point = self.mapToScene(event.pos())
            self.selection_rect = QRectF(self.start_point, self.start_point)
            self.viewport().update()

        elif event.button() == Qt.MouseButton.RightButton:
            print("Rechte Maustaste erkannt - Kontextmenü prüfen")
            view_position = event.pos()  # Speichere die Position im View

            # Überprüfe, ob sich die Maus über einem ObjectiveItem befindet
            found_objective = next(
            (obj for obj in self.objective_manager.list_objectives()
            if obj.sceneBoundingRect().contains(scene_position)), None
            )

            found_strategy = next(
            (obj for obj in self.strategy_manager.list_strategies()
            if obj.sceneBoundingRect().contains(scene_position)), None
            )

            if found_objective:
                print(f"Objective gefunden: {found_objective}")
                self.selected_rect = found_objective  # Speichere das gefundene Objective als ausgewählt
                self.show_new_strategy_context_menu(view_position)  # Zeige das neue Kontextmenü
            elif found_strategy:
                print(f"stratgie gefunden: {found_strategy}")
                self.selected_rect = found_strategy  # Speichere das gefundene Objective als ausgewählt
                self.show_new_measure_context_menu(view_position)  # Zeige das neue Kontextmenü

            else:
                print("Kein Objective gefunden - Zeige Standard-Kontextmenü")
                self.show_empty_context_menu(view_position)  # Zeige das Standard-Kontextmenü

    def mouseMoveEvent(self, event):
        if self.selecting:
            end_point = self.mapToScene(event.pos())
            self.selection_rect = QRectF(self.start_point, end_point).normalized()
            self.viewport().update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.selecting:
            self.selecting = False
            self.selection_rect = QRectF()  # Rahmen zurücksetzen
            self.viewport().update()

# --------------------------------------------------------------
# ---------------- contextmenu events --------------------------
# --------------------------------------------------------------

    def open_objective_dialog(self, position):
        # Erstelle ein Dialogfenster für ein neues Ziel
        dialog = NewObjectiveDialog("New Objective")
        
        # Öffne den Dialog und überprüfe, ob der Benutzer "OK" (Accepted) gedrückt hat
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Extrahiere den Namen und die Beschreibung des neuen Ziels aus dem Dialog
            objective_name, objective_desc = dialog.get_new_values()
            
            # Erstelle ein neues Zielobjekt mit vordefinierten Dimensionen (200x100)
            new_obj = self.objective_manager.create_objective(objective_name, objective_desc, 200, 100)
            
            # Berechne die horizontale Position, um das Objekt in der Mitte der Szene zu platzieren
            # Falls keine Szene existiert, setze die Position auf 0
            center_x = (self.my_scene.sceneRect().width() - new_obj.rect.width()) / 2 if self.scene() else 0
            
            # Setze die berechnete Position für das neue Ziel
            new_obj.setPos(center_x, 10)
            
            # Füge das neue Ziel zur Szene hinzu
            self.my_scene.addItem(new_obj)
            
            # Zentriere die Ansicht auf das neue Ziel
            self.centerOn(new_obj)

    def open_strategy_dialog(self, position):
        """
        Erstellt ein neues StrategyItem und verknüpft es direkt mit dem vorhandenen Objective.
        """
        if self.objective_manager.is_empty():
            print("Kein Objective vorhanden. Strategy kann nicht erstellt werden.")
            return

        dialog = NewStrategyDialog("New Strategy", self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            strategy_name, strategy_desc = dialog.get_new_values()
            new_strategy = self.strategy_manager.create_strategy(strategy_name, strategy_desc, 200, 100, self)
            self.my_scene.addItem(new_strategy)

            # Verknüpfung mit dem ersten vorhandenen Objective
            objective = self.selected_rect
            relationship = self.relationship_manager.create_combine_relationship(
                "Objective-Strategy Relation",
                "Erstellt beim Hinzufügen einer neuen Strategy",
                objective,
                new_strategy
            )
            self.my_scene.addItem(relationship)

            print(f"Neue Strategy erstellt und verknüpft: {new_strategy}")
            self.arrange_items()

    def show_empty_context_menu(self, position
                                 ):
        context_menu = QMenu(self)
        context_menu.addAction(QAction("New Objective...", self, triggered=lambda: self.open_objective_dialog(position)))
        context_menu.exec(self.mapToGlobal(position))

    def open_measure_Dialog(self, position):
        """
        Erstellt ein neues MeasureItem und verknüpft es direkt mit der selektierten Strategy.
        """
        if not self.selected_rect:
            print("Keine Strategy ausgewählt. Measure kann nicht erstellt werden.")
            return

        dialog = NewMeasureDialog("New Measure", self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            measure_name, measure_desc = dialog.get_new_values()
            new_measure = self.measure_manager.create_measure(measure_name, measure_desc, 200, 100)
            self.my_scene.addItem(new_measure)

            # Verknüpfung mit aktuell selektierter Strategy
            if hasattr(self.selected_rect, "strategy"):
                relationship = self.relationship_manager.create_combine_relationship(
                    "Strategy-Measure Relation",
                    "Erstellt beim Hinzufügen einer neuen Measure",
                    self.selected_rect,
                    new_measure
                )
                self.my_scene.addItem(relationship)

                print(f"Neue Measure erstellt und verknüpft: {new_measure}")
                self.arrange_items()
            else:
                print("Ausgewähltes Element ist keine gültige Strategy.")
    
    def show_new_strategy_context_menu(self, position):
        """Zeigt das Kontextmenü für die Erstellung einer neuen Strategie."""
        context_menu = QMenu(self)

        # Menüeintrag für das Erstellen einer neuen Strategie
        new_strategy_action = QAction("New Strategy...", self)
        new_strategy_action.triggered.connect(lambda: self.open_strategy_dialog(position))
        context_menu.addAction(new_strategy_action)

        context_menu.exec(self.mapToGlobal(position))

    def show_new_measure_context_menu(self,position):
        """Zeigt das Kontextmenü für die Erstellung einer neuen Strategie."""
        context_menu = QMenu(self)

        # Menüeintrag für das Erstellen einer neuen Maßnahme
        new_strategy_action = QAction("New measure...", self)
        new_strategy_action.triggered.connect(lambda: self.open_measure_Dialog(position))
        context_menu.addAction(new_strategy_action)

        context_menu.exec(self.mapToGlobal(position))

    def start_drawing(self, position):
        self.selected_rect = None
        self.drawing = True
        self.start_point = position
        self.current_rect = QRectF(position, position)

    def drawForeground(self, painter: QPainter, rect: QRectF):
        if self.selecting:
            painter.setPen(QPen(QColor(0, 255, 0), 2, Qt.PenStyle.DashLine))
            painter.drawRect(self.selection_rect)
        
