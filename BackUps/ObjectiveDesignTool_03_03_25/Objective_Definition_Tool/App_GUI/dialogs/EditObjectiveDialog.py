from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout

class EditObjectiveDialog(QDialog):
    def __init__(self, objective, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Objective")
        self.objective = objective

        # Widgets
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.name_input.setText(self.objective.name)  # Vorbefüllung mit aktuellem Wert
        
        self.desc_label = QLabel("Description:")
        self.desc_input = QLineEdit()
        self.desc_input.setText(self.objective.description)  # Vorbefüllung mit aktuellem Wert
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_and_close)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.desc_label)
        layout.addWidget(self.desc_input)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
    
    def save_and_close(self):
        self.objective.name = self.name_input.text()
        self.objective.description = self.desc_input.text()
        self.accept()  # Schließt den Dialog mit akzeptierter Rückgabe

    def get_updated_objective(self):
        return self.objective