"""Comando ensure_superuser: cria o administrador a partir de variáveis de ambiente."""

import pytest
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core.management import CommandError, call_command

pytestmark = pytest.mark.django_db

STRONG_PASSWORD = "uma-senha-bem-forte-42"


@pytest.fixture
def admin_env(monkeypatch):
    monkeypatch.setenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", STRONG_PASSWORD)
    monkeypatch.delenv("DJANGO_SUPERUSER_USERNAME", raising=False)


def test_creates_superuser_with_verified_email(admin_env):
    call_command("ensure_superuser")

    user = get_user_model().objects.get(email="admin@example.com")
    assert user.is_superuser
    assert user.is_staff
    assert user.username == "admin"
    assert user.check_password(STRONG_PASSWORD)
    assert EmailAddress.objects.filter(
        user=user, email="admin@example.com", verified=True, primary=True
    ).exists()


def test_uses_username_from_environment(admin_env, monkeypatch):
    monkeypatch.setenv("DJANGO_SUPERUSER_USERNAME", "chefe")
    call_command("ensure_superuser")
    assert get_user_model().objects.get(email="admin@example.com").username == "chefe"


def test_does_nothing_when_variables_are_missing(monkeypatch):
    monkeypatch.delenv("DJANGO_SUPERUSER_EMAIL", raising=False)
    monkeypatch.delenv("DJANGO_SUPERUSER_PASSWORD", raising=False)
    call_command("ensure_superuser")
    assert not get_user_model().objects.exists()


def test_is_idempotent_and_keeps_existing_password(admin_env, monkeypatch):
    call_command("ensure_superuser")
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", "outra-senha-bem-forte-99")

    call_command("ensure_superuser")

    user = get_user_model().objects.get(email="admin@example.com")
    assert user.check_password(STRONG_PASSWORD)
    assert get_user_model().objects.count() == 1


def test_rejects_weak_password(admin_env, monkeypatch):
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", "123456")
    with pytest.raises(CommandError):
        call_command("ensure_superuser")
    assert not get_user_model().objects.exists()
