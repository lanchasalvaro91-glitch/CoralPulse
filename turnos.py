import random, json
from datetime import datetime

class TurnoControl:
    def __init__(self, participantes, tiempo_por_turno=180):
        self.participantes = participantes
        self.tiempo_por_turno = tiempo_por_turno
        self.turno_actual = 0
        random.shuffle(self.participantes)
        self.historial = []

    def siguiente_turno(self):
        p = self.participantes[self.turno_actual]
        self.turno_actual = (self.turno_actual + 1) % len(self.participantes)
        reg = {"participante": p, "inicio": datetime.now().isoformat()}
        self.historial.append(reg)
        return reg

    def exportar_json(self, archivo="turnos.json"):
        with open(archivo, "w") as f:
            json.dump(self.historial, f, indent=2)
        return archivo
