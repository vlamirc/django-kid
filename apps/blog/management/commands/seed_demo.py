from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.accounts.roles import Role, grant_role
from apps.blog.models import Post

DEMO_PASSWORD = "senha-de-demonstracao-123"

DEMO_USERS = [
    # (username, e-mail, papel)
    ("editora", "editora@example.com", Role.EDITOR),
    ("autor", "autor@example.com", Role.AUTHOR),
    ("leitora", "leitora@example.com", None),
]

DEMO_POSTS = [
    (
        "Olá, Django!",
        "O primeiro post do blog",
        "Este post foi criado pelo comando seed_demo.\n\n"
        "Explore o código em apps/blog para ver como ele foi feito.",
        Post.Status.PUBLISHED,
    ),
    (
        "Por que TDD?",
        "Escreva o teste primeiro",
        "Primeiro o teste falha, depois o código faz ele passar, "
        "e por fim você melhora o código com segurança.",
        Post.Status.PUBLISHED,
    ),
    ("Um rascunho", "", "Só o autor e os editores veem este post.", Post.Status.DRAFT),
]


class Command(BaseCommand):
    help = "Cria usuários e posts de demonstração. Só para desenvolvimento."

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.filter(username="autor").exists():
            raise CommandError("Os dados de demonstração já existem.")

        users = {}
        for username, email, role in DEMO_USERS:
            user = User.objects.create_user(username, email, DEMO_PASSWORD)
            EmailAddress.objects.create(user=user, email=email, verified=True, primary=True)
            if role:
                grant_role(user, role)
            users[username] = user

        for title, subtitle, body, status in DEMO_POSTS:
            Post.objects.create(
                title=title, subtitle=subtitle, body=body, status=status, author=users["autor"]
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Pronto! Entre com autor@example.com, editora@example.com ou "
                f"leitora@example.com e a senha {DEMO_PASSWORD}"
            )
        )
