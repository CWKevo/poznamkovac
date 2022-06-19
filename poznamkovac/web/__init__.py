import typing as t

import poznamkovac.nastavenia as n

from flask import Flask
from flask_login import LoginManager
from flask_babel import Babel

from sqlmodel import Session, select

from poznamkovac.databaza.engine import DATABAZA
from poznamkovac.databaza.modely import Pouzivatel

from poznamkovac.web.api import api_url_for
from poznamkovac.web.blueprinty import VSETKY_BLUEPRINTY

from poznamkovac.sukromne_nastavenia import SENTRY_DSN, TAJNY_KLUC # type: ignore


if SENTRY_DSN is not None:
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[FlaskIntegration()], traces_sample_rate=1.0)


WEB = Flask(__name__, static_folder='staticke_subory', template_folder='sablony')
WEB.config["SECRET_KEY"] = TAJNY_KLUC
WEB.config['DEBUG'] = n.DEBUG
WEB.config['BABEL_TRANSLATION_DIRECTORIES'] = '../i18n/preklady'

AUTHENTICATION = LoginManager(WEB)
BABEL = Babel(WEB)

for blueprint in VSETKY_BLUEPRINTY:
    WEB.register_blueprint(blueprint)



@WEB.context_processor
def add_additional_context():
    return {
        'api_url_for': api_url_for,
        'APP_NAME': n.NAZOV,
        'APP_VERSION': n.VERZIA
    }



@AUTHENTICATION.user_loader
def load_user(id) -> t.Optional[Pouzivatel]:
    with Session(DATABAZA) as session:
        return session.exec(select(Pouzivatel).where(Pouzivatel.id == id)).first()



if __name__ == '__main__':
    WEB.run(host=n.WEB_HOST, port=n.WEB_PORT, debug=n.DEBUG)
