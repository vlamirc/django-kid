"""Fixtures compartilhadas por todos os testes."""

import pytest
from allauth.mfa.models import Authenticator

from apps.accounts.roles import Role, grant_role
from apps.accounts.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _fast_and_isolated_settings(settings):
    # Hash de senha rápido: Argon2 é lento de propósito e deixaria a suíte lenta.
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    # Sem manifest: os testes não dependem de rodar collectstatic antes.
    settings.STORAGES = {
        **settings.STORAGES,
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
    settings.SECURE_SSL_REDIRECT = False
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


def enable_mfa(user):
    Authenticator.objects.create(user=user, type=Authenticator.Type.TOTP, data={"secret": "x"})
    return user


@pytest.fixture
def reader(db):
    return UserFactory()


@pytest.fixture
def author(db):
    user = UserFactory()
    grant_role(user, Role.AUTHOR)
    return user


@pytest.fixture
def other_author(db):
    user = UserFactory()
    grant_role(user, Role.AUTHOR)
    return user


@pytest.fixture
def editor(db):
    user = UserFactory()
    grant_role(user, Role.EDITOR)
    return enable_mfa(user)


@pytest.fixture
def superuser(db):
    return enable_mfa(UserFactory(is_staff=True, is_superuser=True))
