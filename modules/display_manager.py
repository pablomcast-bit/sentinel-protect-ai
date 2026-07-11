import cv2


class DisplayManager:

    def __init__(self):
        pass

    # ==========================================
    # DIBUJAR ZONAS
    # ==========================================

    def draw_zones(self, frame, zone_manager):

        for name, (x1, y1, x2, y2) in zone_manager.zones.items():

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

            cv2.putText(
                frame,
                name,
                (x1 + 5, y1 + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2
            )

    # ==========================================
    # DIBUJAR DETECCIÓN
    # ==========================================

    def draw_detection(self, frame, detection, zone=None):

        x1, y1, x2, y2 = detection["bbox"]

        person_id = detection.get("id", "?")

        label = f"ID {person_id}"

        if zone:
            label += f" | {zone}"

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    # ==========================================
    # MOSTRAR VENTANA
    # ==========================================

    def show(self, frame):

        cv2.imshow("SENTINEL PROTECT AI", frame)

    # ==========================================
    # CERRAR
    # ==========================================

    def close(self):

        cv2.destroyAllWindows()