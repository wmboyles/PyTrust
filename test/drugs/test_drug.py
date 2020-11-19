# Demonstrates how to test the API

import pytest
from http import HTTPStatus

from src.models.persistent.user.user import User
from src.models.enums.user_role.user_role import UserRole
from src.models.enums.gender.gender import Gender
from src.models.enums.drug_type.drug_type import DrugType


# This method runs every time before each test method
@pytest.fixture(autouse=True)
def before(session, client):
    u = User()
    u.username = "user"
    u.set_password("password")
    u.role = UserRole.ADMIN
    session.add(u)
    session.commit()

    res = client.post(
        "http://localhost:5000/login",
        data={"username": u.username, "password": "password"},
        follow_redirects=True,
    )

    assert res.status_code == HTTPStatus.OK.value


def test_drug(client):
    res = client.get("http://localhost:5000/api/drug_types")
    actual = set(res.json)

    expected = {d.value for d in DrugType}
    assert expected == actual


def test_drug2(client):
    res = client.get("http://localhost:5000/api/genders")
    actual = set(res.json)

    expected = {g.value for g in Gender}
    assert expected == actual
