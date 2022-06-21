import typing as t
import poznamkovac.nastavenia as n

from poznamkovac.sukromne_nastavenia import SENTRY_DSN, TAJNY_KLUC


import fastapi as fa

from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

from starlette.datastructures import URLPath
from starlette.routing import NoMatchFound


import json
from datetime import timedelta
from bcrypt import checkpw
from sqlmodel import Session, select, or_, func
from fastapi.responses import JSONResponse as _JSONResponse


from poznamkovac.funkcie.hashing import hashovat_heslo
from poznamkovac.databaza.engine import DATABAZA
from poznamkovac.databaza.modely import Pouzivatel



class JSONResponse(_JSONResponse):
    """
        Vlastná podtrieda `JSONResponse` z `fastapi.responses`, ktorá vytvára JSON odpovede v štandarizovanom formáte.
    """

    def render(self, obsah: t.Any) -> str:
        chyby = obsah.pop('chyby', None) if isinstance(obsah, dict) else None

        novy_obsah = {
            'uspech': chyby is None,
            'chyby': chyby,
            'data': None if chyby else obsah
        }

        return json.dumps(
            novy_obsah,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")



API = fa.FastAPI(title=f"{n.NAZOV} API", version=n.VERZIA, docs_url="/", redoc_url="/redoc", default_response_class=JSONResponse)



if SENTRY_DSN is not None:
    import sentry_sdk
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

    sentry_sdk.init(dsn=SENTRY_DSN)

    API.add_middleware(SentryAsgiMiddleware)



@API.post("/registracia")
async def autorizacia(prezyvka: str, email: str, heslo: str):
    """
        Registrácia nového používateľa.
    """

    if prezyvka == '' or email == '' or heslo == '':
        return fa.HTTPException(status_code=400, detail="Niektoré z povinných údajov sú prázdne.")

    if 32 < len(heslo) < 8:
        return fa.HTTPException(status_code=400, detail="Heslo musí mať medzi 8 až 32 znakmi.")


    with Session(DATABAZA) as s:
        pouzivatel = s.exec(select(Pouzivatel).where(or_(Pouzivatel.email == email, Pouzivatel.prezyvka == prezyvka))).first()

        if pouzivatel is not None:
            return fa.HTTPException(status_code=400, detail="Používateľ s týmto E-mailom alebo prezývkou už existuje.")
        
        pouzivatel = Pouzivatel(prezyvka=prezyvka, email=email, heslo=hashovat_heslo(heslo))

        s.add(pouzivatel)
        s.commit()

    return pouzivatel.dict()



@API.post('/login')
async def autentifikacia(email: str, heslo: str) -> fa.Response:
    """
        Autentifikácia používateľa.
    """

    with Session(DATABAZA) as s:
        pouzivatel = s.exec(select(Pouzivatel).where(func.lower(Pouzivatel.email) == func.lower(email))).first()


    if pouzivatel is None:
        raise fa.HTTPException(status_code=401, detail="Používateľ neexistuje.", headers={"WWW-Authenticate": "Bearer"})

    if not checkpw(heslo.encode('utf-8'), pouzivatel.heslo.encode('utf-8')):
        fa.HTTPException(status_code=401, detail="Heslo je nesprávne.", headers={"WWW-Authenticate": "Bearer"})


    token = AUTENTIFIKACIA.create_access_token(data={'sub': pouzivatel.id})

    odpoved = fa.Response(status_code=200, content=json.dumps({'token': token}))
    AUTENTIFIKACIA.set_cookie(odpoved, token)
    return odpoved



@API.exception_handler(fa.exceptions.RequestValidationError)
async def validation_exception_handler(_, exception: fa.exceptions.RequestValidationError) -> JSONResponse:
    """
        Vytvorí štandarizovanú odpoveď v prípade chyby, pre konzistenciu.
    """

    return JSONResponse({"errors": exception.errors()}, status_code=400)



AUTENTIFIKACIA = LoginManager(secret=TAJNY_KLUC, token_url='/autentifikacia', cookie_name='autentifikacny_token', use_cookie=True, use_header=False, default_expiry=timedelta(weeks=6))


@AUTENTIFIKACIA.user_loader()
async def nacitat_pouzivatela(user_id: str):
    with Session(DATABAZA) as s:
        return s.exec(select(Pouzivatel).where(Pouzivatel.email == user_id)).first()




from poznamkovac.web.api.routery import VSETKY_ROUTERY
for router in VSETKY_ROUTERY:
    API.include_router(router, prefix=router.prefix)


def api_url_for(name: str, ako_uri: bool=True, **path_params) -> t.Optional[URLPath]:
    for router in VSETKY_ROUTERY:
        try:
            cesta = router.url_path_for(name, **path_params)
            cesta = f"{API.root_path}{cesta}"

            if ako_uri:
                return cesta

            else:
                return f"{'https://' if n.POUZIT_HTTPS else 'http://'}{n.API_DOMENA}{cesta}"

        except NoMatchFound:
            continue

    raise NoMatchFound
