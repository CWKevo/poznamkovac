import typing as t
import sqlmodel as sql

from fastapi import APIRouter, Depends
from poznamkovac.databaza.engine import DATABAZA
from poznamkovac.databaza.modely import Pouzivatel, TematickyCelok, TematickyCelok_Predmet_spojenie, Predmet


TEMATICKE_CELKY_ROUTER = APIRouter(prefix='/tematicke_celky')
from poznamkovac.web.api import AUTENTIFIKACIA



@TEMATICKE_CELKY_ROUTER.post('/')
async def vytvor_tematicky_celok(nazov: str, pouzivatel: Pouzivatel = Depends(AUTENTIFIKACIA)):
    """
        Vytvorí nový tematický celok.
    """

    if pouzivatel.typ == 'student':
        raise Exception('Nemáš oprávnenie vytvoriť tematické celky.')

    tematicky_celok = TematickyCelok(nazov=nazov)
    with sql.Session(DATABAZA) as s:
        s.add(tematicky_celok)
        s.commit()

    return tematicky_celok.dict()



@TEMATICKE_CELKY_ROUTER.get("/")
async def vsetky_tematicke_celky(predmet: t.Optional[str]=None) -> t.List[t.Dict[str, t.Any]]:
    """
        Zoznam všetkých tematických celkov.
    """

    with sql.Session(DATABAZA) as s:
        q = sql.select(TematickyCelok)

        if predmet is not None:
            _predmet = s.exec(sql.select(Predmet).where(sql.func.lower(Predmet.nazov) == sql.func.lower(predmet))).first()
            q = q.join(TematickyCelok_Predmet_spojenie).where(TematickyCelok_Predmet_spojenie.predmet_id == _predmet.id)
        
        return [tc.dict() for tc in s.exec(q).all()]
