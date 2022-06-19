import typing as t
import poznamkovac.nastavenia as s

from poznamkovac.sukromne_nastavenia import SENTRY_DSN

import fastapi as fa
from starlette.datastructures import URLPath
from starlette.routing import NoMatchFound

import json
from fastapi.responses import JSONResponse as _JSONResponse

from poznamkovac.web.api.routery import VSETKY_ROUTERY



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



API = fa.FastAPI(title=f"{s.NAZOV} API", version=s.VERZIA, docs_url="/", redoc_url="/redoc", default_response_class=JSONResponse)

for router in VSETKY_ROUTERY:
    API.include_router(router, prefix=router.prefix)



if SENTRY_DSN is not None:
    import sentry_sdk
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

    sentry_sdk.init(dsn=SENTRY_DSN)

    API.add_middleware(SentryAsgiMiddleware)



@API.exception_handler(fa.exceptions.RequestValidationError)
async def validation_exception_handler(_, exception: fa.exceptions.RequestValidationError):
    """
        Vytvorí štandarizovanú odpoveď v prípade chyby, pre konzistenciu.
    """

    return JSONResponse({"errors": exception.errors()}, status_code=400)



def api_url_for(name: str, ako_uri: bool=True, **path_params) -> t.Optional[URLPath]:
    for router in VSETKY_ROUTERY:
        try:
            cesta = router.url_path_for(name, **path_params)
            cesta = f"{API.root_path}{cesta}"

            if ako_uri:
                return cesta

            else:
                return f"{'https://' if s.POUZIT_HTTPS else 'http://'}{s.API_DOMENA}{cesta}"

        except NoMatchFound:
            continue

    raise NoMatchFound
