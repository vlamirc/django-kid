"""Fluxos de conta: cadastro, verificação de e-mail, login e admin."""

import pytest
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import identify_hasher
from django.core import mail
from django.urls import reverse
from pytest_django.asserts import assertContains, assertRedirects

from apps.accounts.tests.factories import DEFAULT_PASSWORD, UserFactory

pytestmark = pytest.mark.django_db

SIGNUP_URL = reverse("account_signup")
LOGIN_URL = reverse("account_login")


def signup(client, password="uma-senha-bem-forte-42"):
    return client.post(
        SIGNUP_URL,
        {
            "email": "nova@example.com",
            "username": "nova",
            "password1": password,
            "password2": password,
        },
    )


def test_login_page_uses_the_site_layout(client):
    response = client.get(LOGIN_URL)
    assertContains(response, "Acesse sua conta")
    assertContains(response, "clean-blog.css")


def test_signup_sends_a_verification_email(client):
    signup(client)
    assert get_user_model().objects.filter(email="nova@example.com").exists()
    assert len(mail.outbox) == 1
    assert "nova@example.com" in mail.outbox[0].to


@pytest.mark.parametrize(
    "weak_password",
    ["curta1", "123456789012", "password1234"],
    ids=["too-short", "only-numbers", "too-common"],
)
def test_signup_rejects_weak_passwords(client, weak_password):
    response = signup(client, password=weak_password)
    assert response.status_code == 200
    assert not get_user_model().objects.filter(email="nova@example.com").exists()


def test_unverified_user_cannot_log_in(client):
    signup(client)
    client.logout()
    response = client.post(LOGIN_URL, {"login": "nova@example.com", "password": DEFAULT_PASSWORD})
    assertRedirects(response, reverse("account_email_verification_sent"))
    assert "_auth_user_id" not in client.session


def test_verified_user_logs_in_with_email(client):
    user = UserFactory()
    response = client.post(LOGIN_URL, {"login": user.email, "password": DEFAULT_PASSWORD})
    assertRedirects(response, reverse("blog:post_list"))
    assert EmailAddress.objects.get(user=user).verified


def test_user_with_2fa_must_enter_the_code(client):
    from conftest import enable_mfa

    user = enable_mfa(UserFactory())
    response = client.post(LOGIN_URL, {"login": user.email, "password": DEFAULT_PASSWORD})
    assertRedirects(response, reverse("mfa_authenticate"))
    assert "_auth_user_id" not in client.session


def test_passwords_are_hashed_with_argon2(settings):
    settings.PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.Argon2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    ]
    user = UserFactory()
    assert identify_hasher(user.password).algorithm == "argon2"


def test_admin_login_goes_through_the_site_login(client):
    url = reverse("admin:index")
    response = client.get(reverse("admin:login"), {"next": url})
    assertRedirects(response, f"{LOGIN_URL}?next={url}", fetch_redirect_response=False)
