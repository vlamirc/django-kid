from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Usuário do sistema.

    Ainda não tem campos extras, mas existe desde o primeiro dia porque trocar
    o modelo de usuário depois que o projeto está em produção é muito caro.
    Veja https://docs.djangoproject.com/pt-br/5.2/topics/auth/customizing/.
    """

    @property
    def display_name(self) -> str:
        return self.get_full_name() or self.username
