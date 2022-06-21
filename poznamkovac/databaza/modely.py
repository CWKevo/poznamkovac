import typing as t

import sqlmodel as sql
from slugify import slugify



class HlavnyModel(sql.SQLModel, table=False):
    id: t.Optional[int] = sql.Field(default=None, primary_key=True)



class Pouzivatel(HlavnyModel, table=True):
    __tablename__ = 'pouzivatelia'

    prezyvka: str = sql.Field(index=True)
    """Prezývka používateľa."""
    email: str
    """E-mailová adresa používateľa."""
    heslo: str
    """Zahashované heslo používateľa."""

    typ: str = sql.Field(default='student')
    """Typ používateľa (`student`, `ucitel` alebo `admin`)."""


    @property
    def identifikator(self) -> str:
        return f"{slugify(self.prezyvka)}.{self.id}"



class TematickyCelok_Predmet_spojenie(sql.SQLModel, table=True):
    __tablename__ = 'tematickycelok_predmet_spojenie'

    tematicky_celok_id: t.Optional[int] = sql.Field(default=None, foreign_key='tematicke_celky.id', primary_key=True)
    """ID tematického celku"""
    predmet_id: t.Optional[int] = sql.Field(default=None, foreign_key='predmety.id', primary_key=True)
    """ID predmetu, ktorý patrí tematickému celku"""



class TematickyCelok_Ucivo_spojenie(sql.SQLModel, table=True):
    __tablename__ = 'tematickycelok_ucivo_spojenie'

    tematicky_celok_id: t.Optional[int] = sql.Field(default=None, foreign_key='tematicke_celky.id', primary_key=True)
    """ID tematického celku"""
    ucivo_id: t.Optional[int] = sql.Field(default=None, foreign_key='uciva.id', primary_key=True)
    """ID učiva, ktoré patrí tematickému celku"""



class Predmet(HlavnyModel, table=True):
    __tablename__ = 'predmety'

    nazov: str = sql.Field(sa_column_kwargs={'unique': True}, index=True)
    """Názov predmetu"""

    tematicke_celky: t.List['TematickyCelok'] = sql.Relationship(back_populates='predmety', link_model=TematickyCelok_Predmet_spojenie)
    """Tematické celky, ktoré patria predmetu"""



class TematickyCelok(HlavnyModel, table=True):
    __tablename__ = 'tematicke_celky'

    nazov: str = sql.Field(sa_column_kwargs={'unique': True}, index=True)
    """Názov tematického celku"""

    predmety: t.List[Predmet] = sql.Relationship(back_populates='tematicke_celky', link_model=TematickyCelok_Predmet_spojenie)
    """Predmety, ktoré patria tematickému celku"""
    uciva: t.List['Ucivo'] = sql.Relationship(back_populates='tematicke_celky', link_model=TematickyCelok_Ucivo_spojenie)
    """Učivá, ktoré patria tematickému celku"""



class Ucivo(HlavnyModel, table=True):
    __tablename__ = 'uciva'

    nazov: str = sql.Field(sa_column_kwargs={'unique': True}, index=True)
    """Názov učiva."""
    poznamky: t.Text
    """Poznámky k učivu v čistom HTML formáte."""

    tematicke_celky: t.List[TematickyCelok] = sql.Relationship(back_populates='uciva', link_model=TematickyCelok_Ucivo_spojenie)
    """Tematické celky, ktoré patria k učivu"""
