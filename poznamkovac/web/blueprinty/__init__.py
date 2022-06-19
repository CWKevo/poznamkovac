import typing as t

from flask import Blueprint

from poznamkovac.web.blueprinty.hlavny import HLAVNY_BLUEPRINT


VSETKY_BLUEPRINTY: t.List[t.Type[Blueprint]] = [
    HLAVNY_BLUEPRINT
]
