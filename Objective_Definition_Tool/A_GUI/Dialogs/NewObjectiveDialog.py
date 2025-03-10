from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton

class NewObjectiveDialog(QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)

        # Layout erstellen
        layout = QVBoxLayout(self)

        # Eingabefelder für Name und Beschreibung
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Objective Name")
        layout.addWidget(self.name_input)

        self.desc_input = QLineEdit(self)
        self.desc_input.setPlaceholderText("Objective Description")
        layout.addWidget(self.desc_input)

        # OK- und Abbrechen-Buttons
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)

    def get_new_values(self):
        """Liefert die eingegebenen Werte zurück"""
        return self.name_input.text(), self.desc_input.text()
