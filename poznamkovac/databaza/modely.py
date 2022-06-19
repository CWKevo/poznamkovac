import typing as t

import sqlmodel as sql



class HlavnyModel(sql.SQLModel, table=False):
    id: t.Optional[int] = sql.Field(default=None, primary_key=True)



class Pouzivatel_Skupina_spojenie(sql.SQLModel, table=True):
    __tablename__ = 'pouzivatel_skupina_spojenie'

    skupina_id: t.Optional[int] = sql.Field(default=None, foreign_key='skupiny.id', primary_key=True)
    """ID skupiny do ktorej patrí používateľ."""
    clen_id: t.Optional[int] = sql.Field(default=None, foreign_key='pouzivatelia.id', primary_key=True)
    """ID používateľa patriaceho k skupine."""



class Pouzivatel(HlavnyModel, table=True):
    __tablename__ = 'pouzivatelia'

    prezyvka: str
    """Používateľské meno."""
    email: str
    """E-mailová adresa používateľa."""
    heslo: str
    """Zahashované heslo používateľa."""

    skupiny: t.List['Skupina'] = sql.Relationship(back_populates='clenovia', link_model=Pouzivatel_Skupina_spojenie)
    """Zoznam skupín, v ktorých sa používateľ nachádza."""
    vlastnene_skupiny: t.List['Skupina'] = sql.Relationship(back_populates='spravca')
    """Zoznam skupín, ktoré používateľ vytvoril."""



class Skupina(HlavnyModel, table=True):
    __tablename__ = 'skupiny'

    nazov: str
    """Názov skupiny."""
    popis: t.Optional[t.Text]
    """Popis skupiny."""

    clenovia: t.List[Pouzivatel] = sql.Relationship(back_populates='skupiny', link_model=Pouzivatel_Skupina_spojenie)
    """Zoznam používateľov, ktorí sa nachádzajú v skupine."""

    spravca: t.Optional[Pouzivatel] = sql.Relationship(back_populates='vlastnene_skupiny')
    """Používateľ, ktorý vytvoril skupinu."""
    spravca_id: t.Optional[int] = sql.Field(foreign_key='pouzivatelia.id')
    """ID používateľa, ktorý vytvoril skupinu."""



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

    nazov: str = sql.Field(sa_column_kwargs={'unique': True})
    """Názov predmetu"""

    tematicke_celky: t.List['TematickyCelok'] = sql.Relationship(back_populates='predmety', link_model=TematickyCelok_Predmet_spojenie)
    """Tematické celky, ktoré patria predmetu"""



class TematickyCelok(HlavnyModel, table=True):
    __tablename__ = 'tematicke_celky'

    nazov: str = sql.Field(sa_column_kwargs={'unique': True})
    """Názov tematického celku"""

    predmety: t.List[Predmet] = sql.Relationship(back_populates='tematicke_celky', link_model=TematickyCelok_Predmet_spojenie)
    """Predmety, ktoré patria tematickému celku"""
    uciva: t.List['Ucivo'] = sql.Relationship(back_populates='tematicke_celky', link_model=TematickyCelok_Ucivo_spojenie)
    """Učivá, ktoré patria tematickému celku"""



class Ucivo(HlavnyModel, table=True):
    __tablename__ = 'uciva'

    nazov: str = sql.Field(sa_column_kwargs={'unique': True})
    """Názov učiva"""
    poznamky: t.Text
    """Poznámky k učivu"""

    tematicke_celky: t.List[TematickyCelok] = sql.Relationship(back_populates='uciva', link_model=TematickyCelok_Ucivo_spojenie)
    """Tematické celky, ktoré patria k učivu"""
