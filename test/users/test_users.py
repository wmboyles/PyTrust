# Demonstrates how to test the persistnece classes

from src.models.persistent.user.user import User
from src.models.enums.user_role.user_role import UserRole


def test_number(session):
    current_users = User.query.all()
    assert len(current_users) == 0

    u = User()
    u.username = "test_user"
    u.set_password("password")
    u.role = UserRole.PATIENT

    session.add(u)
    session.commit()

    assert u.id > 0

    current_users = User.query.all()
    assert len(current_users) == 1
