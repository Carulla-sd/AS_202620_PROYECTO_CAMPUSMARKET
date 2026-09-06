import sqlite3
import time
from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.publicaciones.repository import initialize_database


client = TestClient(app)


def test_corte_vertical_crea_y_recupera_publicacion(
    tmp_path: Path,
    monkeypatch,
):
    database = tmp_path / "campusmarket-test.db"
    monkeypatch.setenv("CAMPUSMARKET_DB_PATH", str(database))

    payload = {
        "titulo": "Calculadora científica",
        "descripcion": "Calculadora reacondicionada en buen estado",
        "precio": 65000,
        "modalidad": "venta",
        "estado": "reacondicionado",
    }

    create_response = client.post("/publicaciones", json=payload)

    assert create_response.status_code == 201

    created = create_response.json()

    assert created["id"] > 0
    assert created["titulo"] == payload["titulo"]
    assert created["estado"] == "reacondicionado"
    assert database.exists()

    list_response = client.get("/publicaciones")

    assert list_response.status_code == 200

    publicaciones = list_response.json()

    assert len(publicaciones) == 1
    assert publicaciones[0] == created
    assert publicaciones[0]["estado"] == "reacondicionado"


def test_bloqueo_sqlite_degrada_controladamente_y_se_recupera(
    tmp_path: Path,
    monkeypatch,
):
    database = tmp_path / "campusmarket-lock-test.db"
    monkeypatch.setenv("CAMPUSMARKET_DB_PATH", str(database))

    payload = {
        "titulo": "Libro arquitectura",
        "descripcion": "Prueba de bloqueo temporal de SQLite",
        "precio": 50000,
        "modalidad": "venta",
        "estado": "usado",
    }

    initialize_database()

    locker = sqlite3.connect(database)
    locker.execute("BEGIN EXCLUSIVE")

    before = locker.execute(
        "SELECT COUNT(*) FROM publicaciones"
    ).fetchone()[0]

    try:
        start = time.perf_counter()
        blocked_response = client.post("/publicaciones", json=payload)
        blocked_elapsed = time.perf_counter() - start

        after_failed = locker.execute(
            "SELECT COUNT(*) FROM publicaciones"
        ).fetchone()[0]

        assert blocked_response.status_code == 503
        assert blocked_elapsed <= 2.0
        assert after_failed == before

        detail = blocked_response.json()["detail"]
        assert "temporalmente no disponible" in detail.lower()

    finally:
        locker.rollback()
        locker.close()

    recovery_response = client.post("/publicaciones", json=payload)

    assert recovery_response.status_code == 201

    with sqlite3.connect(database) as connection:
        final_count = connection.execute(
            "SELECT COUNT(*) FROM publicaciones"
        ).fetchone()[0]

    assert final_count == before + 1
