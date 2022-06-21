import typing as t
import poznamkovac.nastavenia as n

from warnings import warn
from pathlib import Path
from sqlmodel import create_engine, SQLModel

# Musíme všetky modely preniesť do tohto prostredia, aby ich SQLAlchemy našla.
from poznamkovac.databaza.modely import Pouzivatel, TematickyCelok, TematickyCelok_Predmet_spojenie, TematickyCelok_Ucivo_spojenie, Predmet, Ucivo

try:
    from poznamkovac.sukromne_nastavenia import URI_DATABAZY

except ImportError:
    URI_DATABAZY = None


if URI_DATABAZY:
    DATABAZA = create_engine(URI_DATABAZY, echo=n.DEBUG)

else:
    warn('Nie je nastavená URI databázy. Toto je v poriadku pokiaľ testuješ pomocou pyTestu - použije sa predvolená SQLite databáza...')
    DATABAZA = create_engine(rf"sqlite:///{Path(__file__).parent.parent.parent / 'testy' / 'test_databaza.db'}", echo=n.DEBUG)


VSETKY_MODELY: t.List[t.Type[SQLModel]] = [
    Pouzivatel,

    TematickyCelok,
    TematickyCelok_Predmet_spojenie,
    TematickyCelok_Ucivo_spojenie,

    Predmet,
    Ucivo
]
"""Zoznam všetkých modelov pre databázu."""

SQLModel.metadata.create_all(DATABAZA)
