from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout

class NewStrategyDialog(QDialog):
    def __init__(self, current_name="new strategy", current_description="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Strategy")
        self.setGeometry(150, 150, 300, 200)

        # Layout erstellen
        self.layout = QVBoxLayout()

        # Eingabe für den Strategienamen
        self.label_name = QLabel("Enter new strategy name:")
        self.layout.addWidget(self.label_name)

        self.name_input = QLineEdit(self)
        self.name_input.setText(current_name)
        self.layout.addWidget(self.name_input)

        # Eingabe für die Strategie-Beschreibung
        self.label_description = QLabel("Enter strategy description:")
        self.layout.addWidget(self.label_description)

        self.description_input = QLineEdit(self)
        self.description_input.setText(current_description)
        self.layout.addWidget(self.description_input)

        # OK-Button
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

        # Cancel-Button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

    def get_new_values(self):
        """Gibt den eingegebenen Namen und die Beschreibung zurück."""
        return self.name_input.text(), self.description_input.text()