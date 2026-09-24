# Autorização

Autenticação responde "quem é você?". Autorização responde "o que você pode fazer?".

## Papéis

Cada papel é um `Group` do Django, declarado em `apps/accounts/roles.py`:

| Papel | Pode |
| --- | --- |
| (nenhum, leitor) | Ler posts publicados |
| **Autores** | Escrever posts e editar/excluir os próprios |
| **Editores** | Editar e excluir qualquer post, ver rascunhos de todos |
| Superusuário | Tudo |

Dê ou tire papéis pelo admin (Usuários > Grupos) ou pelo código:

```python
from apps.accounts.roles import Role, grant_role, revoke_role

grant_role(user, Role.AUTHOR)
```

## Regras

As regras usam o [django-rules](https://github.com/dfunckt/django-rules): pequenas funções
(predicados) que se combinam com `&`, `|` e `~`. As do blog estão em `apps/blog/rules.py`:

```python
can_add_post = has_author_role | has_editor_role
can_change_post = (has_author_role & is_post_author) | has_editor_role
can_view_post = is_published | can_change_post
```

E são ligadas às permissões padrão do Django no modelo:

```python
class Meta:
    rules_permissions = {
        "add": blog_rules.can_add_post,
        "view": blog_rules.can_view_post,
        "change": blog_rules.can_change_post,
        "delete": blog_rules.can_change_post,
    }
```

## Usando em todo lugar

A mesma pergunta, `has_perm("blog.change_post", post)`, funciona em qualquer camada:

```python
# Python
request.user.has_perm("blog.change_post", post)

# View baseada em classe
from rules.contrib.views import PermissionRequiredMixin


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "blog.change_post"  # o objeto é verificado automaticamente
```

```django
{# Template #}
{% load rules %}
{% has_perm "blog.change_post" user post as can_change %}
{% if can_change %}<a href="...">Editar</a>{% endif %}
```

No admin, `ObjectPermissionsModelAdmin` aplica as mesmas regras.

Quem não está logado e tenta algo protegido vai para o login; quem está logado e não
tem permissão recebe "Acesso negado" (403).

## Adicionando uma regra nova

1. Escreva a linha na tabela de testes (`test_rules.py`) e veja falhar.
2. Crie o predicado no `rules.py` da app (ou reutilize os de `roles.py`).
3. Ligue ao modelo em `Meta.rules_permissions` (ou use `rules.add_perm` para
   permissões que não são de um modelo).
4. Use `PermissionRequiredMixin` na view e `{% has_perm %}` no template.

**Nunca** escreva `if user.groups.filter(...)` ou `if user.is_staff` numa view ou
template: a regra ficaria espalhada e seria esquecida na próxima mudança.
