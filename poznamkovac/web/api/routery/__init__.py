import typing as t

from fastapi import APIRouter

from poznamkovac.web.api.routery.hlavny import HLAVNY_ROUTER


VSETKY_ROUTERY: t.List[t.Type[APIRouter]] = [
    HLAVNY_ROUTER
]
