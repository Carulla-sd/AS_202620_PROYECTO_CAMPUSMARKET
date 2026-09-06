import os
import sqlite3
import sys
import tempfile
import time
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.app.main import app
from backend.app.publicaciones.repository import initialize_database


PAYLOAD = {
    "titulo": "Libro arquitectura",
    "descripcion": "Medición S5 de bloqueo temporal de SQLite",
    "precio": 50000,
    "modalidad": "venta",
    "estado": "usado",
}


def main() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        database = Path(temp_dir) / "campusmarket-medicion.db"
        os.environ["CAMPUSMARKET_DB_PATH"] = str(database)

        initialize_database()

        client = TestClient(app)

        locker = sqlite3.connect(database)
        locker.execute("BEGIN EXCLUSIVE")

        registros_antes = locker.execute(
            "SELECT COUNT(*) FROM publicaciones"
        ).fetchone()[0]

        inicio = time.perf_counter()
        respuesta_bloqueada = client.post(
            "/publicaciones",
            json=PAYLOAD,
        )
        tiempo_bloqueo = time.perf_counter() - inicio

        registros_despues = locker.execute(
            "SELECT COUNT(*) FROM publicaciones"
        ).fetchone()[0]

        print("=== MEDICION S5: SQLITE BLOQUEADA ===")
        print(f"HTTP durante bloqueo: {respuesta_bloqueada.status_code}")
        print(f"Tiempo durante bloqueo: {tiempo_bloqueo:.3f} s")
        print(f"Registros antes: {registros_antes}")
        print(f"Registros despues del intento: {registros_despues}")
        print(
            "Escritura parcial:",
            "NO" if registros_despues == registros_antes else "SI",
        )
        print(
            "Detalle:",
            respuesta_bloqueada.json().get("detail"),
        )

        locker.rollback()
        locker.close()

        inicio_recuperacion = time.perf_counter()
        respuesta_recuperacion = client.post(
            "/publicaciones",
            json=PAYLOAD,
        )
        tiempo_recuperacion = (
            time.perf_counter() - inicio_recuperacion
        )

        with sqlite3.connect(database) as connection:
            registros_finales = connection.execute(
                "SELECT COUNT(*) FROM publicaciones"
            ).fetchone()[0]

        print()
        print("=== RECUPERACION DESPUES DE LIBERAR SQLITE ===")
        print(
            f"HTTP recuperacion: "
            f"{respuesta_recuperacion.status_code}"
        )
        print(
            f"Tiempo recuperacion: "
            f"{tiempo_recuperacion:.3f} s"
        )
        print(f"Registros finales: {registros_finales}")

        print()
        print("=== RESUMEN PARA EVIDENCIA ===")
        print(
            f"bloqueo_http="
            f"{respuesta_bloqueada.status_code}"
        )
        print(f"bloqueo_segundos={tiempo_bloqueo:.3f}")
        print(
            "escritura_parcial="
            f"{'no' if registros_despues == registros_antes else 'si'}"
        )
        print(
            f"recuperacion_http="
            f"{respuesta_recuperacion.status_code}"
        )
        print(
            f"recuperacion_segundos="
            f"{tiempo_recuperacion:.3f}"
        )

        os.environ.pop("CAMPUSMARKET_DB_PATH", None)


if __name__ == "__main__":
    main()
