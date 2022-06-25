import typing as t

from pathlib import Path
from jinja2 import Environment, PackageLoader


T_ENV = Environment(loader=PackageLoader('poznamkovac.backend', 'sablony'))



def vykreslit_sablonu(subor_sablony: t.Union[Path, str], data: t.Any) -> str:
    """
        Vykreslí obsah zo súboru šablóny.
    """

    sablona = T_ENV.get_template(subor_sablony)
    return sablona.render(data)
