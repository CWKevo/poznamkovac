import typing as t
import poznamkovac.nastavenia as s

from pathlib import Path
from sqlmodel import create_engine, SQLModel

# Musíme všetky modely preniesť do tohto prostredia, aby ich SQLAlchemy našla.
from poznamkovac.databaza.modely import Pouzivatel


CESTA_K_DATABAZE = Path(__file__).parent / 'database.db'
DATABAZA = create_engine(rf'sqlite:///{CESTA_K_DATABAZE.absolute()}', echo=s.DEBUG)


ALL_MODELS: t.List[t.Type[SQLModel]] = [
    Pouzivatel
]
"""Zoznam všetkých modelov pre databázu."""

SQLModel.metadata.create_all(DATABAZA)
