from parking_detect.services.analize import Service
from parking_detect.presentation.ui.main_window import start_app
from parking_detect.application.application_controller import ApplicationController


if __name__ == "__main__":
    application = ApplicationController()
    application.run()
