from poznamkovac.backend.emaily import odoslat_email



def test_emaily():
    """
        Otestuje odosielanie E-mailov
    """

    odoslat_email("Predmet", "<h1>Obsah - test</h1>", "skevo.cw@gmail.com")



if __name__ == '__main__':
    test_emaily()
