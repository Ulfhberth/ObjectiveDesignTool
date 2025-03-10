from PyQt6.QtWidgets import QMenu, QDialog, QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPainter, QAction
from PyQt6.QtCore import Qt, QRectF, QPointF
from A_GUI.Dialogs.NewObjectiveDialog import NewObjectiveDialog
from A_GUI.Dialogs.NewStrategyDialog import NewStrategyDialog
from B_CORE.Entities.objectives.ObjectiveManager import ObjectiveManager
from B_CORE.Entities.strategies.StrategyManager import StrategyManager
from B_CORE.Entities.objectives.Objective import ObjectiveItem
from B_CORE.Entities.strategies.Strategy import StrategyItem


class ObjectiveCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.my_scene = QGraphicsScene(0, 0, 10000, 10000)
        self.setScene(self.my_scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.scale_factor = 1.0
        self.objective_manager = ObjectiveManager()
        self.strategy_manager = StrategyManager()
        self.selected_rect = None
        self.drawing = False
        self.start_point = QPointF()
        self.current_rect = QRectF()

    def arrange_items(self, spacing=50):
        """
        Ordnet alle StrategyItems so an, dass ihr gemeinsamer Mittelpunkt unter dem ObjectiveItem liegt.
        
        :param spacing: Der horizontale Abstand zwischen den StrategyItems (Standard: 50 Pixel)
        """
        # Alle ObjectiveItems in der Szene abrufen (sollte eigentlich nur eines sein)
        objective_items = [item for item in self.my_scene.items() if isinstance(item, ObjectiveItem)]

        if not objective_items:
            print("Kein ObjectiveItem gefunden, Anordnung abgebrochen.")
            return

        # Nehme das erste ObjectiveItem als Referenz
        objective = objective_items[0]
        objective_center_x = objective.sceneBoundingRect().center().x()
        objective_bottom_y = objective.sceneBoundingRect().bottom()

        # Alle StrategyItems abrufen
        strategy_items = [item for item in self.my_scene.items() if isinstance(item, StrategyItem)]

        if not strategy_items:
            print("Keine StrategyItems gefunden.")
            return

        # Gesamtbreite aller StrategyItems + Abstände berechnen
        total_width = sum(item.boundingRect().width() for item in strategy_items) + (len(strategy_items) - 1) * spacing

        # Startposition so setzen, dass die Strategies mittig unter dem Objective erscheinen
        start_x = objective_center_x - (total_width / 2)
        y_position = objective_bottom_y + 50  # 50px unter dem Objective

        # StrategyItems anordnen
        for strategy in strategy_items:
            strategy.setPos(start_x, y_position)
            start_x += strategy.boundingRect().width() + spacing  # Nächstes Item rechts positionieren

        print(f"{len(strategy_items)} StrategyItems wurden unter dem Objective angeordnet.")


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

    def open_strategy_dialog(self, position):
        # Erstelle ein Dialogfenster für eine neue Strategie
        dialog = NewStrategyDialog("New Strategy")
        
        # Öffne den Dialog und überprüfe, ob der Benutzer "OK" (Accepted) gedrückt hat
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Extrahiere den Namen und die Beschreibung der neuen Strategie aus dem Dialog
            strategy_name, strategy_desc = dialog.get_new_values()
            
            # Erstelle ein neues StrategyItem mit vordefinierten Dimensionen (200x100)
            new_strategy = self.strategy_manager.create_strategy(strategy_name, strategy_desc, 200, 100)
            
            # Füge die neue Strategie zur Szene hinzu
            self.my_scene.addItem(new_strategy)

            self.arrange_items()

            # Berechne die horizontale Position, um das Objekt in der Mitte der Szene zu platzieren
            # center_x = (self.my_scene.sceneRect().width() - new_strategy.rect.width()) / 2 if self.scene() else 0
            
            # Setze die berechnete Position für die neue Strategie
            # new_strategy.setPos(center_x, 300)
            
            # Zentriere die Ansicht auf die neue Strategie
            # self.centerOn(new_strategy)



    def show_empty_context_menu(self, position):
        context_menu = QMenu(self)
        context_menu.addAction(QAction("New Objective...", self, triggered=lambda: self.open_objective_dialog(position)))
        context_menu.exec(self.mapToGlobal(position))

    def show_new_strategy_context_menu(self, position):
        """Zeigt das Kontextmenü für die Erstellung einer neuen Strategie."""
        context_menu = QMenu(self)

        # Menüeintrag für das Erstellen einer neuen Strategie
        new_strategy_action = QAction("New Strategy...", self)
        new_strategy_action.triggered.connect(lambda: self.open_strategy_dialog(position))
        context_menu.addAction(new_strategy_action)

        context_menu.exec(self.mapToGlobal(position))

    def start_drawing(self, position):
        self.selected_rect = None
        self.drawing = True
        self.start_point = position
        self.current_rect = QRectF(position, position)

    
        
