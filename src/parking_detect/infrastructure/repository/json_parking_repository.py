
import json
import os
import logging


class JsonParkingRepository:
    def __init__(self, file_path):
        self.file_path = file_path
        self._check_file()

    def _check_file(self) -> None:
        if not os.path.exists(self.file_path):
            logging.error("File Path Error")

    def get_spots(self):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        return data