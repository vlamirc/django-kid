import os

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = (
        "Cria o administrador a partir de DJANGO_SUPERUSER_EMAIL e DJANGO_SUPERUSER_PASSWORD "
        "(e, opcionalmente, DJANGO_SUPERUSER_USERNAME). Não faz nada se as variáveis não "
        "existirem ou se o usuário já existir. Pensado para plataformas sem shell."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")
        if not email or not password:
            self.stdout.write("ensure_superuser: variáveis não definidas, nada a fazer.")
            return

        User = get_user_model()
        if User.objects.filter(email__iexact=email).exists():
            self.stdout.write(f"ensure_superuser: {email} já existe, nada a fazer.")
            return

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME") or email.split("@")[0]
        user = User(username=username, email=email)
        try:
            validate_password(password, user)
        except ValidationError as error:
            raise CommandError(
                f"Senha do administrador fraca: {' '.join(error.messages)}"
            ) from error

        user = User.objects.create_superuser(username, email, password)
        # O login exige e-mail verificado; o administrador já nasce verificado.
        EmailAddress.objects.create(user=user, email=email, verified=True, primary=True)
        self.stdout.write(self.style.SUCCESS(f"ensure_superuser: administrador {email} criado."))
