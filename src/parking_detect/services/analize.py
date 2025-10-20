import cv2
import numpy as np
from parking_detect.data.frame_processor import FrameProcessor


class Service:
    def __init__(self, video_path):
        self.video_path = video_path
        self.parking_spots = []

    def check_spot_occupancy(self, frame, spot_coords):
        pts = np.array(spot_coords, np.int32).reshape((-1, 1, 2))

        mask = np.zeros(frame.shape[:2], np.uint8)
        cv2.fillPoly(mask, [pts], 255)

        mean_val = cv2.mean(frame, mask=mask)[0]

        return mean_val < 80
    
    def mark_spots(self, frame, grayscale_frame):
        ...

    def run(self):
        cap = cv2.VideoCapture(self.video_path)

        while True:
            ret, frame = cap.read()
            if not ret: 
                break

            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_handler = FrameProcessor(frame)
            done_frame = frame_handler.detect_spots()
            
            cv2.imshow("frame", done_frame)

            # for i, spot in enumerate(self.parking_spots):
            #     occupied = self.check_spot_occupancy(frame, spot)
            #     color = (0, 0, 255) if occupied else (0, 255, 0)

            #     pts = np.array(spot, np.int32).reshape((-1, 1, 2))
            #     cv2.polylines(frame, [pts], True, color, 2)
            #     cv2.putText(frame, str(i), (spot[0], spot[1]-10), 
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                
            # cv2.imshow('Parking', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
                



    



