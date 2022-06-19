NAZOV = "Poznámkovač"
"""Názov aplikácie"""
VERZIA = "0.0.1"
"""The application version. Bude to použité v API a pri CSS súboroch v `<link/>` (cache problém - https://stackoverflow.com/a/12992803)."""

WEB_HOST = 'localhost'
"""Host pre web."""
WEB_PORT = 5000
"""Port pre web."""
WEB_DOMENA = 'www.example.com'
"""Doména (v produkcii). Toto sa použije pre vytvorenie správnych presmerovaní v frontende."""

API_HOST = 'localhost'
"""Host pre API server."""
API_PORT = 5001
"""Port pre API server."""
API_DOMENA = 'www.example.com/api'
"""Doména pre API (v produkcii). Toto sa použije pre vytvorenie správnych presmerovaní v frontende."""

POUZIT_HTTPS = False
"""Majú sa použiť `https://` schémy?"""

DEBUG = True
"""Vypľuvne info naviac pri chode aplikácie."""
