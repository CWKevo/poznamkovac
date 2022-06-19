from sqlmodel import create_engine, SQLModel
from poznamkovac.databaza.engine import VSETKY_MODELY


TEST_DATABAZA = create_engine('sqlite:///:memory:')
SQLModel.metadata.create_all(TEST_DATABAZA)


if __name__ == '__main__':
    print(VSETKY_MODELY)
