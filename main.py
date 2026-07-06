import cv2

from modules.camera_manager import CameraManager
from modules.detector import Detector
from modules.zone_manager import ZoneManager
from modules.display_manager import DisplayManager
from modules.event_engine import EventEngine


def main():

    print("=" * 50)
    print("SENTINEL PROTECT AI")
    print("=" * 50)

    camera = CameraManager()
    detector = Detector()
    display = DisplayManager()
    zones = ZoneManager()
    events = EventEngine()

    # ===========================
    # ZONAS
    # ===========================

    zones.add_zone("PUERTA", 0, 0, 200, 480)
    zones.add_zone("INTERIOR", 220, 100, 420, 400)
    zones.add_zone("VENTANA", 440, 0, 640, 480)

    person_detected = False

    while True:

        frame = camera.read()

        if frame is None:
            break

        detections = detector.detect(frame)

        display.draw_zones(frame, zones)

        person_detected = False

        for detection in detections:

            if detection["class"] != "person":
                continue

            zone = zones.get_zone(detection["bbox"])

            display.draw_detection(
                frame,
                detection,
                zone
            )

            if zone is not None:

                person_detected = True

                if not events.recording:

                    events.start(
                        frame,
                        zone
                    )

        if events.recording:

            events.update(frame)

        if events.recording and not person_detected:

            events.stop()

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