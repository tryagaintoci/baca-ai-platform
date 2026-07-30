from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Importer tous les modèles pour les enregistrer dans Base.metadata
import app.models  # noqa: E402, F401
