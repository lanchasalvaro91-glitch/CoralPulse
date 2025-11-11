import json, requests, os
from metrics_logger import MetricasLogger
from turnos import TurnoControl

COMET_API_KEY = os.getenv("COMET_API_KEY")
PROJECT_NAME = "CoralPulse"

def main():
    # 1. Simulamos una sesión rápida
    turnos = TurnoControl(["Ana", "Carlos", "IA-1"])
    logger = MetricasLogger("sesion_demo")

    for _ in range(3):
        turnos.siguiente_turno()
        logger.registrar_intervencion("Ana", 60, "pregunta")
        logger.registrar_intervencion("Carlos", 50, "afirmacion")
        logger.registrar_reformulacion("Ana", "Carlos", True)

    # 2. Guardamos métricas
    logger.exportar_json()
    turnos.exportar_json()

    # 3. Subimos a Comet (si hay clave)
    if COMET_API_KEY:
        experiment = {"apiKey": COMET_API_KEY, "projectName": PROJECT_NAME, "metrics": logger.generar_reporte()}
        response = requests.post("https://www.comet.com/api/rest/v1/write", json=experiment)
        if response.status_code == 200:
            print("✅ Métricas enviadas a Comet")
        else:
            print(f"Error al enviar datos a Comet: {response.status_code}")
    else:
        print("No hay clave de API de Comet")

if __name__ == "__main__":
    main()
