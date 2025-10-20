import numpy as np
import cv2
import json
import os
import time


class FrameProcessor:
    def __init__(self, frame):
        self.frame = frame
        self.clone = frame.copy()
        self.points = [] # [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        self.parking_spots = []
        self.current_spot_id = 1
        self.last_call_time = time.time()

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print("TOUCH")
            self.points.append((x, y))

            cv2.circle(self.clone, (x, y), 5, (0, 255, 0), -1)

            if len(self.points) == 4:
                self.complete_parking_spot()
        elif event == cv2.EVENT_RBUTTONDOWN: # Delete spots
            self.points = []
            self.clone = self.frame.copy()

    def complete_parking_spot(self):
        if len(self.points) == 4:
            spot = {
                "id": self.current_spot_id,
                "points": self.points.copy()
            }
        self.parking_spots.append(spot)
        self.draw_spot(spot)
        self.current_spot_id += 1
        self.points = []

    def convert_to_grayscale(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contour_image = frame.copy()
        contour_image[:] = 0
        cv2.drawContours(contour_image, contours, -1, (255, 255, 255), thickness=2)
        return contour_image

    def check_spots_occupancy(self):
        if not self.parking_spots:
            return
        current_time = time.time()
        elapsed_time = current_time - self.last_call_time
        threshold = 30

        free_spots = 0
        for spot in self.parking_spots:
            print(spot)
            xs = [point[0] for point in spot["points"]]
            ys = [point[1] for point in spot["points"]]
            print(xs)

        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)

        x1 = x_min + 10
        x2 = x_max - 10
        y1 = y_min + 10
        y2 = y_max

        start_point, stop_point = (x1, y1), (x2, y2)

        grayscale_frame = self.convert_to_grayscale(self.clone)
        crop = grayscale_frame[y1:y2, x1:x2]
        cv2.imshow("T", crop)
        gray_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        cv2.imshow("S", gray_crop)
        
        count = cv2.countNonZero(gray_crop)
        print(count)
        color, thick = [(0, 255, 0), 5] if count < threshold else [(0, 0, 255), 2]

        if count < threshold:
            free_spots += 1

        cv2.rectangle(self.clone, start_point, stop_point, color, thick)

        current_time = time.time()

    def draw_spot(self, spot):
        points_array = np.array(spot["points"], np.int32)
        cv2.polylines(self.clone, [points_array], True, (0, 255, 0), 2)
        print("DRAW", self.parking_spots)
        # Put The Text
        # center_x = sum([p[0] for p in spot["points"]]) // 4
        # center_y = sum([p[1] for p in spot["points"]]) // 4
        # cv2.putText(self.clone, str(self.current_spot_id), (center_x, center_y),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    def save_spots(self):
        data = {
            "parking_spots": self.parking_spots
        }
        print(data)
        
        try:
            with open("data/parking_spots.json", 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print("SAVE ERROR: {e}")

    def load_spots(self, filename="data/parking_spots.json") -> bool:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                print("LOAD", data)
                self.parking_spots = data["parking_spots"]
                self.current_spot_id = len(self.parking_spots) + 1
            return True
        return False

    def draw_all_spots(self, frame) -> None:
        for spot in self.parking_spots:
            points = spot["points"]
            points_array = np.array(points, np.int32)
            cv2.polylines(frame, [points_array], True, (0, 255, 0), 2)
        return frame
            
    def detect_spots(self):
        cv2.namedWindow("SPOTS DETECT")
        cv2.setMouseCallback("SPOTS DETECT", self.mouse_callback)
        self.load_spots()

        while True:
            self.check_spots_occupancy()
            frame_with_spots = self.draw_all_spots(self.clone)

            cv2.imshow("SPOTS DETECT", frame_with_spots)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('s'):
                print(self.parking_spots)
                self.save_spots()
                break
            elif key == ord('q'):
                break


        cv2.destroyAllWindows()
