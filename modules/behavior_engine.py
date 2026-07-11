import time


class BehaviorEngine:

    def __init__(self):

        self.states = {}

        self.triggered = {}

        self.loitering_seconds = 5

    # =====================================
    # ANALIZAR
    # =====================================

    def analyze(self, zone):

        now = time.time()

        if zone not in self.states:

            self.states[zone] = now

            self.triggered[zone] = False

            return 0

        elapsed = now - self.states[zone]

        # Solo dispara UNA vez

        if elapsed >= self.loitering_seconds:

            if not self.triggered[zone]:

                self.triggered[zone] = True

                return 30

        return 0

    # =====================================
    # RESETEAR
    # =====================================

    def reset(self, zone):

        if zone in self.states:

            del self.states[zone]

        if zone in self.triggered:

            del self.triggered[zone]