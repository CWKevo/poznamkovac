SENTRY_DSN = None
"""DSN adresa pre [Sentry](https://sentry.io/). Ak je `None`, tak sa Sentry nespustí."""

TAJNY_KLUC = "tajny"
"""Tajný kľúč pre Flask."""

URI_DATABAZY = None
"""SQLAlchemy URI pre databázu."""

EMAIL_HOST = 'smtp.gmail.com'
"""Host pre E-mailový server."""
EMAIL_PORT = 465
"""Port pre E-mailový server."""
EMAIL_USER = ...
"""E-mailový používateľ."""
EMAIL_HESLO = ...
"""Heslo pre používateľa."""
