from PyQt6.QtCore import QPoint

class ObjectiveManager:
    def __init__(self):
        self.objectives = []
    
    def add_objective(self, position: QPoint, name: str):
        """Fügt ein neues Objective hinzu."""
        self.objectives.append((position, name))
    
    def clear(self):
        """Löscht alle Objectives."""
        self.objectives.clear()
    
    def get_objectives(self):
        """Gibt die Liste der Objectives zurück."""
        return self.objectives
    
    def is_empty(self):
        """Überprüft, ob keine Objectives vorhanden sind."""
        return len(self.objectives) == 0
