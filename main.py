import cv2

from modules.camera_manager import CameraManager
from modules.detector import Detector
from modules.zone_manager import ZoneManager
from modules.display_manager import DisplayManager
from modules.event_engine import EventEngine
from modules.behavior_engine import BehaviorEngine
from modules.risk_engine import RiskEngine
from modules.tracker import Tracker


def main():

    print("=" * 50)
    print("SENTINEL PROTECT AI")
    print("=" * 50)

    camera = CameraManager()
    detector = Detector()
    display = DisplayManager()
    zones = ZoneManager()
    events = EventEngine()
    behavior = BehaviorEngine()
    risk = RiskEngine()
    tracker = Tracker()

    # ===========================
    # ZONAS
    # ===========================

    zones.add_zone("PUERTA", 0, 0, 200, 480)
    zones.add_zone("INTERIOR", 220, 100, 420, 400)
    zones.add_zone("VENTANA", 440, 0, 640, 480)

    while True:

        frame = camera.read()

        if frame is None:
            break

        # Actualizar buffer de video
        events.update_buffer(frame)

        # Detectar personas
        detections = detector.detect(frame)

        detections = [

            d for d in detections

            if d["class"] == "person"

        ]

        # Asignar IDs
        detections = tracker.update(detections)

        display.draw_zones(frame, zones)

        person_detected = False

        for detection in detections:

            zone = zones.get_zone(detection["bbox"])

            person_detected = True

            display.draw_detection(
                frame,
                detection,
                zone
            )

            x1, y1, x2, y2 = detection["bbox"]

            # ===========================
            # INFORMACIÓN DEL TRACKER
            # ===========================

            cv2.putText(

                frame,

                f"{detection['time']:.1f}s",

                (x1, y2 + 20),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.6,

                (255, 255, 0),

                2

            )

            cv2.putText(

                frame,

                f"{detection['speed']:.0f}px/s",

                (x1, y2 + 40),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.6,

                (0, 255, 255),

                2

            )

            cv2.putText(

                frame,

                f"R:{tracker.get_risk(detection['id'])}",

                (x1, y2 + 60),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.6,

                (0, 0, 255),

                2

            )

            if zone is None:
                continue

            tracker.update_zone(
                detection["id"],
                zone
            )

            points = behavior.analyze(zone)

            if points > 0:

                tracker.add_risk(
                    detection["id"],
                    points
                )

                risk.add(points)

            if risk.alert() and not events.recording:

                events.start(
                    frame,
                    zone
                )

        # ===========================
        # VIDEO
        # ===========================

        if events.recording:

            events.update(frame)

        if events.recording and not person_detected:

            events.stop()

        # ===========================
        # RESET
        # ===========================

        if not person_detected:

            behavior.reset("PUERTA")
            behavior.reset("INTERIOR")
            behavior.reset("VENTANA")

            risk.reset()

        # ===========================
        # RIESGO GLOBAL
        # ===========================

        cv2.putText(

            frame,

            f"RIESGO GLOBAL: {risk.get_score()}",

            (15, 30),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0, 0, 255),

            2

        )

        display.show(frame)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord("q"):
            break

    if events.recording:

        events.stop()

    camera.release()

    display.close()


if __name__ == "__main__":

    main()