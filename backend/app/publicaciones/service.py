from .repository import (
    PersistenceUnavailableError,
    create_publication,
    list_publications,
)


class PublicationPersistenceUnavailableError(RuntimeError):
    """No es posible guardar publicaciones temporalmente."""


def crear_publicacion(data: dict) -> dict:
    normalized = {
        "titulo": data["titulo"].strip(),
        "descripcion": data["descripcion"].strip(),
        "precio": float(data["precio"]),
        "modalidad": data["modalidad"],
        "estado": data["estado"],
    }

    try:
        return create_publication(normalized)
    except PersistenceUnavailableError as error:
        raise PublicationPersistenceUnavailableError(
            "No es posible guardar la publicación temporalmente."
        ) from error


def listar_publicaciones() -> list[dict]:
    return list_publications()
