import os
import sqlite3
from contextlib import closing
from pathlib import Path


SQLITE_TIMEOUT_SECONDS = 0.5


class PersistenceUnavailableError(RuntimeError):
    """La persistencia no está disponible temporalmente."""


def _db_path() -> Path:
    configured = os.getenv("CAMPUSMARKET_DB_PATH")

    if configured:
        return Path(configured)

    return Path(__file__).resolve().parents[2] / "data" / "campusmarket.db"


def _connect() -> sqlite3.Connection:
    path = _db_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        path,
        timeout=SQLITE_TIMEOUT_SECONDS,
    )
    connection.row_factory = sqlite3.Row

    return connection


def _is_database_locked(error: sqlite3.OperationalError) -> bool:
    error_code = getattr(error, "sqlite_errorcode", None)

    if error_code in {
        sqlite3.SQLITE_BUSY,
        sqlite3.SQLITE_LOCKED,
    }:
        return True

    message = str(error).lower()

    return (
        "database is locked" in message
        or "database table is locked" in message
    )


def initialize_database() -> None:
    with closing(_connect()) as connection, connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS publicaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                precio REAL NOT NULL CHECK (precio > 0),
                modalidad TEXT NOT NULL
                    CHECK (modalidad IN ('venta', 'alquiler')),
                estado TEXT NOT NULL
                    CHECK (
                        estado IN (
                            'nuevo',
                            'usado',
                            'reacondicionado'
                        )
                    )
            )
            """
        )


def create_publication(data: dict) -> dict:
    try:
        initialize_database()

        with closing(_connect()) as connection, connection:
            cursor = connection.execute(
                """
                INSERT INTO publicaciones (
                    titulo,
                    descripcion,
                    precio,
                    modalidad,
                    estado
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    data["titulo"],
                    data["descripcion"],
                    data["precio"],
                    data["modalidad"],
                    data["estado"],
                ),
            )

            publication_id = cursor.lastrowid

            row = connection.execute(
                """
                SELECT
                    id,
                    titulo,
                    descripcion,
                    precio,
                    modalidad,
                    estado
                FROM publicaciones
                WHERE id = ?
                """,
                (publication_id,),
            ).fetchone()

    except sqlite3.OperationalError as error:
        if _is_database_locked(error):
            raise PersistenceUnavailableError(
                "La persistencia está temporalmente no disponible."
            ) from error

        raise

    return dict(row)


def list_publications() -> list[dict]:
    initialize_database()

    with closing(_connect()) as connection, connection:
        rows = connection.execute(
            """
            SELECT
                id,
                titulo,
                descripcion,
                precio,
                modalidad,
                estado
            FROM publicaciones
            ORDER BY id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]
