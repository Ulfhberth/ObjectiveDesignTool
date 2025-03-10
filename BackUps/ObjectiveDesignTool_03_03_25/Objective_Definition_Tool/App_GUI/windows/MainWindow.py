### gui.py
import sys
import os
from PyQt6.QtWidgets import QMainWindow, QTabWidget
from PyQt6.QtGui import QAction 
from PyQt6.QtCore import Qt

from App_GUI.components.Canvas import Canvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Fullscreen Canvas")
        self.setWindowState(Qt.WindowState.WindowMaximized)
        
        # Menüleiste erstellen
        menubar = self.menuBar()
        menubar.setStyleSheet("background-color: black; color: white;")
        file_menu = menubar.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        minimize_action = QAction("Minimize", self)
        minimize_action.triggered.connect(self.showMinimized)
        file_menu.addAction(minimize_action)
        
        # Tab-Widget für mehrere Canvas
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        # Erste Canvas hinzufügen
        self.add_new_tab()
        
        self.setCentralWidget(self.tabs)
        
        # Menüpunkt für neue Tabs
        new_tab_action = QAction("New Canvas", self)
        new_tab_action.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_tab_action)
    
    def add_new_tab(self):
        new_canvas = Canvas()
        tab_index = self.tabs.addTab(new_canvas, f"Canvas {self.tabs.count() + 1}")
        self.tabs.setCurrentIndex(tab_index)
        
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
