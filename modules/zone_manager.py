class ZoneManager:

    def __init__(self):

        self.zones = {}

    # ==============================
    # AGREGAR ZONA
    # ==============================

    def add_zone(self, name, x1, y1, x2, y2):

        self.zones[name] = (x1, y1, x2, y2)

    # ==============================
    # DETECTAR EN QUÉ ZONA ESTÁ
    # ==============================

    def get_zone(self, bbox):

        x1, y1, x2, y2 = bbox

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        for name, (zx1, zy1, zx2, zy2) in self.zones.items():

            if zx1 <= cx <= zx2 and zy1 <= cy <= zy2:

                return name

        return None