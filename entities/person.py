from datetime import datetime


class Person:

    def __init__(self, person_id, bbox):

        self.id = person_id

        self.bbox = bbox

        self.center = self.calculate_center(bbox)

        self.created = datetime.now()

        self.last_seen = datetime.now()

        self.time_in_scene = 0

        self.speed = 0

        self.acceleration = 0

        self.direction = "UNKNOWN"

        self.zone = None

        self.previous_zone = None

        self.state = "OBSERVANDO"

        self.risk = 0

        self.face_id = None

        self.name = "Desconocido"

        self.photos = []

        self.videos = []

        self.history = []

    # =======================================
    # CALCULAR CENTRO
    # =======================================

    def calculate_center(self, bbox):

        x1, y1, x2, y2 = bbox

        return (

            (x1 + x2) // 2,

            (y1 + y2) // 2

        )

    # =======================================
    # ACTUALIZAR DETECCIÓN
    # =======================================

    def update_detection(self, bbox):

        self.bbox = bbox

        self.center = self.calculate_center(bbox)

        self.last_seen = datetime.now()

        self.time_in_scene = (

            self.last_seen - self.created

        ).total_seconds()

    # =======================================
    # CAMBIAR ZONA
    # =======================================

    def set_zone(self, zone):

        if zone != self.zone:

            self.previous_zone = self.zone

            self.zone = zone

            self.add_history(

                f"Entró a {zone}"

            )

    # =======================================
    # AGREGAR RIESGO
    # =======================================

    def add_risk(self, points):

        self.risk += points

    # =======================================
    # CAMBIAR ESTADO
    # =======================================

    def set_state(self, state):

        if state != self.state:

            self.state = state

            self.add_history(

                f"Estado -> {state}"

            )

    # =======================================
    # HISTORIAL
    # =======================================

    def add_history(self, text):

        self.history.append({

            "time": datetime.now(),

            "event": text

        })

    # =======================================
    # RESUMEN
    # =======================================

    def summary(self):

        return {

            "id": self.id,

            "name": self.name,

            "zone": self.zone,

            "state": self.state,

            "risk": self.risk,

            "speed": self.speed,

            "time": self.time_in_scene

        }