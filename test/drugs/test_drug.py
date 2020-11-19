from src.models.persistent.drug.drug import Drug
from src.models.enums.drug_type.drug_type import DrugType


def test_drug(session):
    d = Drug()
    d.name = "name"
    d.code = "1111-1111-11"
    d.description = "description"
    d.type = DrugType.Generic

    session.add(d)
    session.commit()

    assert d.id > 0

    d2 = Drug.query.get(d.id)
    assert d == d2


def number2(session):
    pass