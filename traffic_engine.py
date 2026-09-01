import cv2
import numpy as np

from ultralytics import YOLO

from config import (
    YOLO_MODEL,
    VEHICLE_CLASSES,
    CONFIDENCE_THRESHOLD
)


class TrafficEngine:

    def __init__(self):

        self.model = YOLO(YOLO_MODEL)

        self.previous_positions = {}

        self.vehicle_speeds = []


    def process_frame(self, frame):

        results = self.model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=CONFIDENCE_THRESHOLD,
            verbose=False
        )

        vehicle_count = 0

        vehicle_types = {
            "car": 0,
            "motorcycle": 0,
            "bus": 0,
            "truck": 0
        }

        speeds = []


        if not results:
            return frame, self.get_empty_result()


        result = results[0]


        if result.boxes is None:
            return frame, self.get_empty_result()


        boxes = result.boxes


        for box in boxes:

            class_id = int(box.cls[0])

            if class_id not in VEHICLE_CLASSES:
                continue


            vehicle_type = VEHICLE_CLASSES[class_id]

            confidence = float(box.conf[0])


            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )


            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)


            vehicle_count += 1

            vehicle_types[vehicle_type] += 1


            # Tracking ID
            track_id = None

            if box.id is not None:
                track_id = int(box.id[0])


            # Approximate speed
            speed = self.calculate_speed(
                track_id,
                center_x,
                center_y
            )


            if speed is not None:
                speeds.append(speed)


            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )


            label = (
                f"{vehicle_type} "
                f"{confidence:.2f}"
            )


            if track_id is not None:

                label += f" ID:{track_id}"


            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )


        average_speed = (
            float(np.mean(speeds))
            if speeds
            else 0.0
        )


        result_data = {

            "vehicle_count": vehicle_count,

            "vehicle_types": vehicle_types,

            "average_speed": round(
                average_speed,
                2
            )
        }


        return frame, result_data


    def calculate_speed(
        self,
        track_id,
        x,
        y
    ):

        if track_id is None:
            return None


        current_position = (x, y)


        if track_id not in self.previous_positions:

            self.previous_positions[
                track_id
            ] = current_position

            return None


        previous_x, previous_y = (
            self.previous_positions[
                track_id
            ]
        )


        distance = np.sqrt(
            (x - previous_x) ** 2 +
            (y - previous_y) ** 2
        )


        self.previous_positions[
            track_id
        ] = current_position


        # Approximate pixel movement.
        # This is later calibrated to real-world distance.
        speed = distance * 0.1


        return speed


    def get_empty_result(self):

        return {

            "vehicle_count": 0,

            "vehicle_types": {
                "car": 0,
                "motorcycle": 0,
                "bus": 0,
                "truck": 0
            },

            "average_speed": 0
        }