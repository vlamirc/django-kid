import pytest
from django.contrib.auth.models import Group

from apps.accounts.roles import Role, grant_role, is_privileged, revoke_role
from apps.accounts.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_role_groups_are_created_by_migration():
    assert set(Group.objects.values_list("name", flat=True)) >= {Role.AUTHOR, Role.EDITOR}


def test_grant_and_revoke_role():
    user = UserFactory()
    grant_role(user, Role.EDITOR)
    assert user.groups.filter(name=Role.EDITOR).exists()
    revoke_role(user, Role.EDITOR)
    assert not user.groups.exists()


@pytest.mark.parametrize(
    ("attrs", "role", "expected"),
    [
        ({}, None, False),
        ({}, Role.AUTHOR, False),
        ({}, Role.EDITOR, True),
        ({"is_staff": True}, None, True),
        ({"is_superuser": True}, None, True),
    ],
)
def test_is_privileged(attrs, role, expected):
    user = UserFactory(**attrs)
    if role:
        grant_role(user, role)
    assert is_privileged(user) is expected
