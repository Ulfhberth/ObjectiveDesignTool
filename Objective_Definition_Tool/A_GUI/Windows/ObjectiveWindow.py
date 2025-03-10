from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout

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
