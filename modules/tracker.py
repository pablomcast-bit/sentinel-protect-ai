import math
import time


class Tracker:

    def __init__(self):

        self.next_id = 1

        self.objects = {}

        self.max_distance = 80

    # =====================================
    # CENTRO
    # =====================================

    def center(self, bbox):

        x1, y1, x2, y2 = bbox

        return (

            (x1 + x2) // 2,

            (y1 + y2) // 2

        )

    # =====================================
    # DISTANCIA
    # =====================================

    def distance(self, p1, p2):

        return math.sqrt(

            (p1[0]-p2[0])**2 +

            (p1[1]-p2[1])**2

        )

    # =====================================
    # ACTUALIZAR
    # =====================================

    def update(self, detections):

        now = time.time()

        updated = {}

        for detection in detections:

            center = self.center(
                detection["bbox"]
            )

            assigned = False

            for obj_id, obj in self.objects.items():

                dist = self.distance(

                    center,

                    obj["center"]

                )

                if dist < self.max_distance:

                    elapsed = now - obj["last_time"]

                    speed = 0

                    if elapsed > 0:

                        speed = dist / elapsed

                    updated[obj_id] = {

                        "center": center,

                        "bbox": detection["bbox"],

                        "created": obj["created"],

                        "last_time": now,

                        "speed": speed,

                        "zone": obj["zone"],

                        "risk": obj["risk"]

                    }

                    detection["id"] = obj_id

                    detection["speed"] = speed

                    detection["time"] = now - obj["created"]

                    detection["risk"] = obj["risk"]

                    assigned = True

                    break

            if not assigned:

                obj_id = self.next_id

                self.next_id += 1

                updated[obj_id] = {

                    "center": center,

                    "bbox": detection["bbox"],

                    "created": now,

                    "last_time": now,

                    "speed": 0,

                    "zone": None,

                    "risk": 0

                }

                detection["id"] = obj_id

                detection["speed"] = 0

                detection["time"] = 0

                detection["risk"] = 0

        self.objects = updated

        return detections

    # =====================================
    # ACTUALIZAR ZONA
    # =====================================

    def update_zone(self, person_id, zone):

        if person_id in self.objects:

            self.objects[person_id]["zone"] = zone

    # =====================================
    # SUMAR RIESGO
    # =====================================

    def add_risk(self, person_id, points):

        if person_id in self.objects:

            self.objects[person_id]["risk"] += points

    # =====================================
    # OBTENER RIESGO
    # =====================================

    def get_risk(self, person_id):

        if person_id in self.objects:

            return self.objects[person_id]["risk"]

        return 0