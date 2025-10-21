from parking_detect.infrastructure.repository.json_parking_repository import JsonParkingRepository
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal, Slot
from parking_detect.presentation.views.ui_main import Ui_MainWindow
import logging
import sys


class MainWindow(QMainWindow, Ui_MainWindow):
    clicked_spot_signal = Signal(QPushButton)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Indigo Parking Detector")
        self.json_parking_repository = JsonParkingRepository("data/parking_spots.json")
        self._create_spots_widgets()


    def _create_spots_widgets(self):
        data = self.json_parking_repository.get_spots()
        parking_spots = data["parking_spots"]
        for spot in parking_spots:
            frame_spot = QFrame(self.scrollAreaParkingSpots)
            frame_spot.setFrameShape(QFrame.Shape.StyledPanel)
            frame_spot.setFrameShadow(QFrame.Shadow.Raised)
            horizontalLayout_frame_spot = QHBoxLayout(frame_spot)

            label_spot_id = QLabel(frame_spot)
            label_spot_id.setFont(QFont("Arial", 12, QFont.Bold))
            label_spot_id.setText(f"Spot {spot['id']}")

            pushButton_display_info = QPushButton(frame_spot)
            pushButton_display_info.setText("Display")
            pushButton_display_info.setObjectName(f"displaySpot_{spot['id']}")

            horizontalLayout_frame_spot.addWidget(label_spot_id)
            horizontalLayout_frame_spot.addWidget(pushButton_display_info)
            self.verticalLayout_2.addWidget(frame_spot)

            # pushButton_display_info.clicked.connect(self.clicked_spot_signal.emit)
            pushButton_display_info.clicked.connect(
                lambda checked, spot=spot: self.on_btn_spot_clicked(spot)
                )
            
            print(spot)

    @Slot()
    def on_btn_spot_clicked(self, spot: dict):
        print(spot)




def start_app() -> None:
    logging.info("Start application")
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


