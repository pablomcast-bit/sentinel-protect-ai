class RiskEngine:

    def __init__(self):

        self.score = 0

    # ============================
    # SUMAR RIESGO
    # ============================

    def add(self, points):

        self.score += points

    # ============================
    # OBTENER RIESGO
    # ============================

    def get_score(self):

        return self.score

    # ============================
    # REINICIAR
    # ============================

    def reset(self):

        self.score = 0

    # ============================
    # ¿HAY ALERTA?
    # ============================

    def alert(self):

        return self.score >= 100