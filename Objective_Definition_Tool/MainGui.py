### gui.py
import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMenu, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QFont,  QAction 
from PyQt6.QtCore import Qt, QPoint, QRect
from objectives import ObjectiveManager

class EditObjectiveDialog(QDialog):
    def __init__(self, current_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Objective")
        self.setGeometry(150, 150, 300, 150)

        self.layout = QVBoxLayout()

        self.label = QLabel("Enter new objective name:")
        self.layout.addWidget(self.label)

        self.name_input = QLineEdit(self)
        self.name_input.setText(current_name)  # Zeigt den aktuellen Namen an
        self.layout.addWidget(self.name_input)

        # Buttons für Bestätigung oder Abbruch
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

    def get_new_name(self):
        """Gibt den eingegebenen Namen zurück"""
        return self.name_input.text()


class ObjectiveWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Objective Editor")
        self.setGeometry(100, 100, 400, 250)
        
        self.layout = QVBoxLayout()
        self.label = QLabel("Objective Name: Default Name")
        self.layout.addWidget(self.label)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        
class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: gray;")
        self.rectangles = []  # saves rectangles and the name
        self.objective_manager = ObjectiveManager()
        self.selected_rect = None
    
    def mousePressEvent(self, event):
        print("Button clicked")  # Debugging
        print(f"Klick-Position: {event.pos()}")  # Debugging

        if event.button() == Qt.MouseButton.LeftButton:
            print("Left Mouse Button Clicked")  # Debugging
            
            self.selected_rect = None
            self.update()

        elif event.button() == Qt.MouseButton.RightButton:
            print("Right Mouse Button Clicked")  # Debugging
            for rect, name in self.rectangles:
                if rect.contains(event.pos()):  
                    self.selected_rect = rect  
                    print(f"Ausgewähltes Objekt: {name}")  
                    print("Rectangle Context Menu Shown")  # Debugging
                    self.showRectangleContextMenu(event.pos())       
                    self.update()  
                return  # Verhindert, dass das Kontextmenü erscheint, wenn ein Objekt ausgewählt wurde

            # Falls kein Rechteck getroffen wurde
            if self.objective_manager.is_empty():    
                print("Empty Context Menu Shown")  # Debugging
                self.showEmptyContextMenu(event.pos())  
            
            self.selected_rect = None

        self.update()     
    
    def showEmptyContextMenu(self, position):
        context_menu = QMenu(self)
        #child = self.childAt(position)
        
        new_objective_action = QAction("New Objective...", self)
        new_objective_action.triggered.connect(lambda: self.openObjectiveDialog(position))
        context_menu.addAction(new_objective_action)

        context_menu.exec(self.mapToGlobal(position))
    
    def open_edit_dialog(self):
    
        if self.selected_rect:
            # Finde das ausgewählte Objekt und dessen Namen
            for rect, name in self.rectangles:
                if rect == self.selected_rect:
                    current_name = name
                    break
            else:
                return  # Falls kein Objekt gefunden wird, abbrechen

            dialog = EditObjectiveDialog(current_name, self)
            if dialog.exec():  # Falls "OK" geklickt wurde
                new_name = dialog.get_new_name()
                
                # Aktualisiere das Ziel im ObjectiveManager
                self.objective_manager.update_objective(self.selected_rect.topLeft(), new_name)
                self.update()


    def showRectangleContextMenu(self, position):
        context_menu = QMenu(self)
            
        edit_objective_action = QAction("Edit Objective", self)
        edit_objective_action.triggered.connect(self.open_edit_dialog)
        context_menu.addAction(edit_objective_action)
            
        delete_objective_action = QAction("Delete Objective", self)
        delete_objective_action.triggered.connect(self.clearObjectives)
        context_menu.addAction(delete_objective_action)
        
        context_menu.exec(self.mapToGlobal(position))

    def openObjectiveDialog(self, position):
        dialog = ObjectiveDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            objective_name = dialog.get_objective_name()
            self.objective_manager.add_objective(position, objective_name)
            self.update()
    
    def clearObjectives(self):
        self.objective_manager.clear()
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        font = QFont("Arial", 12)

        # delete the old list, to update the new ones
        self.rectangles.clear()    
                
        # set painter configuration
        painter.setBrush(QBrush(QColor(200, 200, 200)))
        painter.setPen(QPen(Qt.GlobalColor.black))
        
        for position, name in self.objective_manager.get_objectives():
            rect_width, rect_height = 200, 100
            rect = QRect(position.x(), position.y(), rect_width, rect_height)
            
            self.rectangles.append((rect, name))

            if self.selected_rect == rect:
                painter.setPen(QPen(Qt.GlobalColor.red, 3))  # Dicke rote Linie
            else:
                painter.setPen(QPen(Qt.GlobalColor.black, 1))
                        
            painter.drawRect(rect)
            font.setUnderline(True)
            painter.setFont(font)
            text_x = position.x() + rect_width // 2 - painter.fontMetrics().horizontalAdvance(name) // 2
            text_y = position.y() + rect_height // 4 + painter.fontMetrics().height() // 4
            painter.drawText(text_x, text_y, name)

        return

        # Falls außerhalb aller Rechtecke geklickt wurde, Auswahl zurücksetzen

class FullScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Fullscreen Canvas")
        self.setWindowState(Qt.WindowState.WindowMaximized)
        
        menubar = self.menuBar()
        menubar.setStyleSheet("background-color: black; color: white;")
        file_menu = menubar.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        minimize_action = QAction("Minimize", self)
        minimize_action.triggered.connect(self.showMinimized)
        file_menu.addAction(minimize_action)
        
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    window.show()
    sys.exit(app.exec())
