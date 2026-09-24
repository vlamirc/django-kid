"""
Papéis (roles) do sistema.

Cada papel é um `Group` do Django. As regras de autorização (arquivos
`rules.py` de cada app) perguntam "o usuário tem o papel X?" em vez de
depender de permissões salvas no banco, então o código é a fonte da verdade.
"""

from enum import StrEnum

import rules
from django.contrib.auth.models import Group


class Role(StrEnum):
    AUTHOR = "Autores"
    EDITOR = "Editores"


def grant_role(user, role: Role) -> None:
    group, _ = Group.objects.get_or_create(name=role)
    user.groups.add(group)


def revoke_role(user, role: Role) -> None:
    user.groups.remove(*Group.objects.filter(name=role))


# Predicados reutilizáveis em todas as apps.
has_author_role = rules.is_group_member(Role.AUTHOR)
has_editor_role = rules.is_group_member(Role.EDITOR)
is_privileged = rules.is_superuser | rules.is_staff | has_editor_role
