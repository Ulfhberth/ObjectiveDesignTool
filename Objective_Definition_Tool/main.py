import sys
from PyQt6.QtWidgets import QApplication
from A_GUI.Windows.MainWindow import FullScreenWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    window.show()
    sys.exit(app.exec())
