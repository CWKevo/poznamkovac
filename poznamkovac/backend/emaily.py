import typing as t
import smtplib, ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from poznamkovac.nastavenia import NAZOV
from poznamkovac.sukromne_nastavenia import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_HESLO


from poznamkovac.backend.sablonovanie import vykreslit_sablonu



def odoslat_email(predmet: str, obsah: str, prijmatel: t.Union[str, t.List[str]], odosielatel: str=EMAIL_USER) -> None:
    """
        Odošle E-mail na zadanú adresu príjmateľov.
    """

    message = MIMEMultipart("alternative")
    message["Subject"] = predmet
    message["From"] = f"{NAZOV}"
    message["To"] = prijmatel if isinstance(prijmatel, str) else ','.join(prijmatel)

    message.attach(MIMEText(obsah, "html"))

    ssl_kontext = ssl.create_default_context()
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=ssl_kontext) as server:
        server.login(odosielatel, EMAIL_HESLO)
        server.sendmail(odosielatel, message["To"], message.as_string())



def vytvorit_email(titulok: str, texty: t.Union[str, t.List[str]], text_tlacidla: t.Optional[str]=None, href_tlacidla: t.Optional[str]=None, pata: str="(c) Poznámkovač. Tento E-mail si dostal pretože máš v Poznámkovači vytvorený účet.") -> str:
    """
        Vytvorí E-mail zo všeobecnej šablóny.
    """

    return vykreslit_sablonu("email.html", titulok=titulok, texty=[texty] if isinstance(texty, str) else texty, text_tlacidla=text_tlacidla, href_tlacidla=href_tlacidla, pata=pata)
