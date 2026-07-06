from ultralytics import YOLO

from config import (
    YOLO_MODEL,
    PERSON_CONFIDENCE
)


class Detector:

    def __init__(self):

        print("Cargando modelo YOLO...")

        self.model = YOLO(str(YOLO_MODEL))

        print("✅ YOLO cargado")

    def detect(self, frame):

        results = self.model(
            frame,
            verbose=False
        )

        detections = []

        for box in results[0].boxes:

            cls = int(box.cls[0])

            confidence = float(box.conf[0])

            if confidence < PERSON_CONFIDENCE:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            detections.append({

                "class": self.model.names[cls],

                "confidence": confidence,

                "bbox": (x1, y1, x2, y2)

            })

        return detections