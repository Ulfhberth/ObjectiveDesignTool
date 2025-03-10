from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction 
from PyQt6.QtCore import Qt
from A_GUI.Scenes.ObjectiveCanvas import ObjectiveCanvas 

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
        
        self.canvas = ObjectiveCanvas()
        self.setCentralWidget(self.canvas)