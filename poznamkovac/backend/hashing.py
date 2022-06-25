from bcrypt import hashpw, gensalt


def hashovat_heslo(heslo: str) -> str:
    """
        Zašifruje/zahashuje heslo pomocou [bcrypt](https://pypi.org/project/bcrypt/).
    """

    return hashpw(heslo.encode('utf-8'), gensalt()).decode('utf-8')
