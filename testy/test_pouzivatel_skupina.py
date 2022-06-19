from sqlmodel import Session, select
from bcrypt import checkpw

from poznamkovac.funkcie.hashing import hashovat_heslo

from testy import TEST_DATABAZA
from poznamkovac.databaza.modely import Pouzivatel, Skupina



def test_pouzivatel_skupina():
    """
        Otestuje vytváranie a načítanie používateľa a skupín.
    """

    with Session(TEST_DATABAZA) as s:
        II_D = Skupina(nazov='II. D')
        III_C = Skupina(nazov='III. C')
        I_K = Skupina(nazov='I. K')

        mrkvickovac = Pouzivatel(prezyvka='Mrkvickovac', email='mrkva@pistek.gov', heslo=hashovat_heslo('123456789'), skupiny=[II_D], vlastnene_skupiny=[II_D])
        pistek = Pouzivatel(prezyvka='Pistek', email='pistek@mrkva.gov', heslo=hashovat_heslo('123456789'), skupiny=[I_K, III_C])

        s.add(mrkvickovac)
        s.add(pistek)
        s.commit()

        s.refresh(mrkvickovac)
        s.refresh(pistek)

        assert checkpw(b'123456789', mrkvickovac.heslo.encode('utf-8'))
        print(mrkvickovac.prezyvka, 'OK')
        print(mrkvickovac.vlastnene_skupiny, 'OK')
        print(pistek.skupiny[0].nazov, 'OK')


        s.delete(mrkvickovac)
        s.delete(pistek)

        s.delete(II_D)
        s.delete(III_C)
        s.delete(I_K)

        s.commit()



if __name__ == '__main__':
    test_pouzivatel_skupina()
