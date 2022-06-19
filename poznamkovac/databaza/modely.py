import typing as t

import sqlmodel as sql



class HlavnyModel(sql.SQLModel, table=False):
    id: t.Optional[int] = sql.Field(default=None, primary_key=True)



class Pouzivatel(HlavnyModel, table=True):
    prezyvka: str
    """Používateľské meno."""
    email: str
    """E-mailová adresa používateľa."""
    heslo: str
    """Zahashované heslo používateľa."""
