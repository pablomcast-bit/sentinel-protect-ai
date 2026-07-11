import math
import time

from entities.person import Person


class TrackerV3:

    def __init__(self):

        self.people = {}

        self.next_id = 1

        self.max_distance = 80

        self.max_missing_time = 2.0

    # =====================================
    # CENTRO DEL BBOX
    # =====================================

    def get_center(self, bbox):

        x1, y1, x2, y2 = bbox

        return (

            (x1 + x2) // 2,

            (y1 + y2) // 2

        )

    # =====================================
    # DISTANCIA ENTRE DOS PUNTOS
    # =====================================

    def distance(self, p1, p2):

        return math.sqrt(

            (p1[0] - p2[0]) ** 2 +

            (p1[1] - p2[1]) ** 2

        )

    # =====================================
    # BUSCAR PERSONA MÁS CERCANA
    # =====================================

    def find_closest(self, bbox):

        center = self.get_center(bbox)

        best_person = None

        best_distance = self.max_distance

        for person in self.people.values():

            d = self.distance(

                center,

                person.center

            )

            if d < best_distance:

                best_distance = d

                best_person = person

        return best_person

    # =====================================
    # CREAR PERSONA NUEVA
    # =====================================

    def create_person(self, bbox):

        person = Person(

            self.next_id,

            bbox

        )

        self.people[self.next_id] = person

        self.next_id += 1

        return person
    # =====================================
    # ACTUALIZAR TRACKER
    # =====================================

    def update(self, detections):

        now = time.time()

        assigned = set()

        results = []

        for detection in detections:

            bbox = detection["bbox"]

            person = self.find_closest(bbox)

            # ---------------------------------
            # Persona nueva
            # ---------------------------------

            if person is None:

                person = self.create_person(bbox)

            else:

                previous_center = person.center

                previous_time = person.last_seen

                person.update_detection(bbox)

                dt = (
                    person.last_seen - previous_time
                ).total_seconds()

                if dt > 0:

                    dist = self.distance(

                        previous_center,

                        person.center

                    )

                    person.speed = dist / dt

            assigned.add(person.id)

            detection["person"] = person

            results.append(detection)

        # ---------------------------------
        # Eliminar personas desaparecidas
        # ---------------------------------

        remove = []

        for person_id, person in self.people.items():

            if person_id in assigned:

                continue

            elapsed = (

                now - person.last_seen.timestamp()

            )

            if elapsed > self.max_missing_time:

                remove.append(person_id)

        for person_id in remove:

            del self.people[person_id]

        return results
    # =====================================
    # ACTUALIZAR ZONA
    # =====================================

    def update_zone(self, person_id, zone):

        if person_id not in self.people:
            return

        self.people[person_id].set_zone(zone)

    # =====================================
    # SUMAR RIESGO
    # =====================================

    def add_risk(self, person_id, points):

        if person_id not in self.people:
            return

        self.people[person_id].add_risk(points)

    # =====================================
    # OBTENER PERSONA
    # =====================================

    def get_person(self, person_id):

        return self.people.get(person_id)

    # =====================================
    # OBTENER TODAS LAS PERSONAS
    # =====================================

    def get_people(self):

        return list(self.people.values())

    # =====================================
    # CONTAR PERSONAS
    # =====================================

    def count(self):

        return len(self.people)

    # =====================================
    # LIMPIAR TRACKER
    # =====================================

    def clear(self):

        self.people.clear()

        self.next_id = 1        