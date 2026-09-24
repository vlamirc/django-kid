import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from apps.accounts.roles import Role, grant_role
from apps.accounts.tests.factories import UserFactory
from conftest import enable_mfa

pytestmark = pytest.mark.django_db

HOME = reverse("blog:post_list")


@pytest.fixture
def editor_without_mfa():
    user = UserFactory()
    grant_role(user, Role.EDITOR)
    return user


def test_privileged_user_without_mfa_is_sent_to_enable_it(client, editor_without_mfa):
    client.force_login(editor_without_mfa)
    assertRedirects(client.get(HOME), reverse("mfa_index"))


def test_staff_without_mfa_cannot_reach_admin(client):
    client.force_login(UserFactory(is_staff=True))
    assertRedirects(client.get(reverse("admin:index")), reverse("mfa_index"))


def test_privileged_user_with_mfa_passes(client, editor_without_mfa):
    client.force_login(enable_mfa(editor_without_mfa))
    assert client.get(HOME).status_code == 200


@pytest.mark.parametrize("url", ["/contas/2fa/", "/contas/logout/", "/healthz/"])
def test_account_pages_stay_reachable(client, editor_without_mfa, url):
    client.force_login(editor_without_mfa)
    assert client.get(url).status_code == 200


def test_regular_users_are_not_affected(client, reader, author):
    for user in (reader, author):
        client.force_login(user)
        assert client.get(HOME).status_code == 200


def test_can_be_turned_off(client, settings, editor_without_mfa):
    settings.MFA_REQUIRED_FOR_PRIVILEGED_USERS = False
    client.force_login(editor_without_mfa)
    assert client.get(HOME).status_code == 200
