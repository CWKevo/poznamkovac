from poznamkovac.backend.emaily import odoslat_email, vytvorit_email



def test_email():
    """
        Otestuje odosielanie E-mailov
    """

    obsah = vytvorit_email('Testovací E-mail', texty=['Ahoj!', 'Toto je testovací E-mail.', 'Zdá sa, že to funguje!', '- Poznámkovač'], text_tlacidla='Tlačidlo', href_tlacidla='https://poznamkovac.kevo.link/')
    return odoslat_email("Predmet", obsah, "skevo.cw@gmail.com")



if __name__ == '__main__':
    test_email()
    print('E-mail bol odoslaný!')
