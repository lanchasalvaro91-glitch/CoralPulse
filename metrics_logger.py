import json
from collections import defaultdict
from datetime import datetime

class MetricasLogger:
    def __init__(self, session_id):
        self.session_id = session_id
        self.intervenciones = []
        self.reformulaciones = []

    def registrar_intervencion(self, participante, duracion, tipo):
        self.intervenciones.append({"participante": participante, "duracion": duracion, "tipo": tipo})

    def registrar_reformulacion(self, original, reformulado, correcta):
        self.reformulaciones.append({"original": original, "reformulado": reformulado, "correcta": correcta})

    def generar_reporte(self):
        tiempo = defaultdict(int)
        preg = defaultdict(int)
        afir = defaultdict(int)
        for i in self.intervenciones:
            tiempo[i["participante"]] += i["duracion"]
            if i["tipo"] == "pregunta": preg[i["participante"]] += 1
            if i["tipo"] == "afirmacion": afir[i["participante"]] += 1
        reform_ok = sum(1 for r in self.reformulaciones if r["correcta"])
        reform_pct = (reform_ok / max(len(self.reformulaciones), 1)) * 100
        return {
            "reformulacion_correcta_pct": round(reform_pct, 2),
            "tiempo_palabra": dict(tiempo),
            "apertura_cognitiva": {p: {"preguntas": preg[p], "afirmaciones": afir[p]} for p in tiempo}
        }

    def exportar_json(self, archivo="metricas.json"):
        with open(archivo, "w") as f:
            json.dump(self.generar_reporte(), f, indent=2)
        return archivo
