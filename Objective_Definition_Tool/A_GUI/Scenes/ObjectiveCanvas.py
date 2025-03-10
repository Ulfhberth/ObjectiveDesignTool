from PyQt6.QtWidgets import QMenu, QDialog, QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPainter, QAction
from PyQt6.QtCore import Qt, QRectF, QPointF
from A_GUI.Dialogs.NewObjectiveDialog import NewObjectiveDialog
from A_GUI.Dialogs.NewStrategyDialog import NewStrategyDialog
from B_CORE.Entities.objectives.ObjectiveManager import ObjectiveManager
from B_CORE.Entities.strategies.StrategyManager import StrategyManager
from B_CORE.Entities.objectives.Objective import ObjectiveItem
from B_CORE.Entities.strategies.Strategy import StrategyItem
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
        self.relationship_manager = RelationshipManager()
        self.selected_rect = None
        self.drawing = False
        self.start_point = QPointF()
        self.current_rect = QRectF()

    def clear_relationships(self):
        """Entfernt alle RelationshipItems aus der Szene."""
        for relationship in self.relationship_manager.list_relationships():
            self.my_scene.removeItem(relationship)
        self.relationship_manager.clear()
  
    def arrange_items(self, spacing_y=50):
        """
        Ordnet alle Objectives und Strategies zentriert an:
        - Objective bleibt oben in der Mitte.
        - Strategies werden mittig unterhalb des Objectives angeordnet.
        - Relationships (Pfeile) werden nach dem Anordnen neu gezeichnet.
        """
        self.clear_relationships()  # Entferne alte Pfeile

        objectives = self.objective_manager.list_objectives()
        strategies = self.strategy_manager.list_strategies()

        if not objectives or not strategies:
            print("Keine Objectives oder Strategies vorhanden. Anordnung nicht möglich.")
            return

        # **Schritt 1:** Positioniere das Objective oben zentriert
        scene_width = self.my_scene.sceneRect().width()
        objective = objectives[0]  # Erstes Objective als zentrales Element
        obj_x = (scene_width - objective.boundingRect().width()) / 2
        obj_y = 50  # Abstand vom oberen Rand
        objective.setPos(obj_x, obj_y)

        # **Schritt 2:** Positioniere alle StrategyItems direkt unter dem Objective
        total_width = sum(strategy.boundingRect().width() for strategy in strategies) + (len(strategies) - 1) * 20
        start_x = (scene_width - total_width) / 2  # Zentrierte Startposition
        strat_y = obj_y + objective.boundingRect().height() + spacing_y

        x_offset = start_x

        for strategy in strategies:
            strategy.setPos(x_offset, strat_y)
            x_offset += strategy.boundingRect().width() + 20  # 20px Abstand zwischen Strategies

            # **Schritt 3:** Erstelle eine neue Combine Relationship
            combine_relationship = self.relationship_manager.create_combine_relationship(
                "Objective-Strategy Relation",
                "Automatische Verbindung",
                objective,
                strategy
            )
            self.my_scene.addItem(combine_relationship)
    
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
            self.start_drawing(scene_position)  # Starte das Zeichnen eines neuen Elements

        elif event.button() == Qt.MouseButton.RightButton:
            print("Rechte Maustaste erkannt - Kontextmenü prüfen")
            view_position = event.pos()  # Speichere die Position im View

            # Überprüfe, ob sich die Maus über einem ObjectiveItem befindet
            found_objective = next(
            (obj for obj in self.objective_manager.list_objectives()
            if obj.sceneBoundingRect().contains(scene_position)), None
            )

            if found_objective:
                print(f"Objective gefunden: {found_objective}")
                self.selected_rect = found_objective  # Speichere das gefundene Objective als ausgewählt
                self.show_new_strategy_context_menu(view_position)  # Zeige das neue Kontextmenü
            else:
                print("Kein Objective gefunden - Zeige Standard-Kontextmenü")
                self.show_empty_context_menu(view_position)  # Zeige das Standard-Kontextmenü

    def mouseMoveEvent(self, event):
        if self.drawing:
            end_point = self.mapToScene(event.pos())
            self.current_rect = QRectF(self.start_point, end_point).normalized()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            self.current_rect = QRectF()

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

    def openStrategyDialog(self, position):
        """
        Erstellt ein neues StrategyItem und ruft `arrange_items()` auf,
        um die Struktur und Relationships zu aktualisieren.
        """
        if self.objective_manager.is_empty():
            print("Kein Objective vorhanden. Strategy kann nicht erstellt werden.")
            return

        dialog = NewStrategyDialog("New Strategy", self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            strategy_name, strategy_desc = dialog.get_new_values()
            new_strategy = self.strategy_manager.create_strategy(strategy_name, strategy_desc, 200, 100, self)
            self.my_scene.addItem(new_strategy)

            print(f"Neue Strategy erstellt: {new_strategy}")

            self.arrange_items()  # Alle Items neu anordnen & Relationships zeichnen


    def show_empty_context_menu(self, position):
        context_menu = QMenu(self)
        context_menu.addAction(QAction("New Objective...", self, triggered=lambda: self.open_objective_dialog(position)))
        context_menu.exec(self.mapToGlobal(position))

    def show_new_strategy_context_menu(self, position):
        """Zeigt das Kontextmenü für die Erstellung einer neuen Strategie."""
        context_menu = QMenu(self)

        # Menüeintrag für das Erstellen einer neuen Strategie
        new_strategy_action = QAction("New Strategy...", self)
        new_strategy_action.triggered.connect(lambda: self.openStrategyDialog(position))
        context_menu.addAction(new_strategy_action)

        context_menu.exec(self.mapToGlobal(position))

    def start_drawing(self, position):
        self.selected_rect = None
        self.drawing = True
        self.start_point = position
        self.current_rect = QRectF(position, position)

    
        
