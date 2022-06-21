from sqlmodel import Session
from bcrypt import checkpw

from poznamkovac.funkcie.hashing import hashovat_heslo

from testy import TEST_DATABAZA
from poznamkovac.databaza.modely import Pouzivatel



def test_pouzivatel():
    """
        Otestuje vytváranie a načítanie používateľa.
    """

    with Session(TEST_DATABAZA) as s:
        mrkvickovac = Pouzivatel(prezyvka='Mrkvickovac', email='mrkva@pistek.gov', heslo=hashovat_heslo('123456789'))
        pistek = Pouzivatel(prezyvka='Pistek', email='pistek@mrkva.gov', heslo=hashovat_heslo('123456789'))

        s.add(mrkvickovac)
        s.add(pistek)
        s.commit()

        s.refresh(mrkvickovac)
        s.refresh(pistek)

        assert checkpw(b'123456789', mrkvickovac.heslo.encode('utf-8'))
        print(mrkvickovac.prezyvka, 'OK')


        s.delete(mrkvickovac)
        s.delete(pistek)

        s.commit()



if __name__ == '__main__':
    test_pouzivatel()
