from sqlmodel import Session, select
from bcrypt import checkpw

from poznamkovac.funkcie.hashing import hashovat_heslo

from testy import TEST_DATABAZA
from poznamkovac.databaza.modely import Pouzivatel



def test_pouzivatel():
    """
        Otestuje vytváranie a načítanie používateľa.
    """

    with Session(TEST_DATABAZA) as s:
        s.add(Pouzivatel(prezyvka='Mrkvickovac', email='mrkva@pistek.gov', heslo=hashovat_heslo('123456789'))) # nikdy neukladaj do databázy heslo "len-tak"!
        s.commit()

        user = s.exec(select(Pouzivatel).where(Pouzivatel.email == 'mrkva@pistek.gov')).first()
        assert checkpw(b'123456789', user.heslo.encode('utf-8'))
        print(user.prezyvka, 'OK')

        s.delete(user)
        s.commit()



if __name__ == '__main__':
    test_pouzivatel()
