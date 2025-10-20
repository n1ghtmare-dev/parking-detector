from PySide6.QtWidgets import QApplication, QMainWindow
from parking_detect.presentation.views.ui_main import Ui_MainWindow
import logging
import sys


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Indigo Parking Detector")


def start_app() -> None:
    logging.info("Start application")
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


