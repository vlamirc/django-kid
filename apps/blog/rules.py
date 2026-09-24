"""
Regras de autorização do blog (django-rules).

Leia como frases: "pode alterar um post quem é autor e dono do post, ou quem
é editor". As regras ficam em código, com testes, e valem em todo lugar:
views (`PermissionRequiredMixin`), templates (`{% has_perm %}`), admin e
`user.has_perm("blog.change_post", post)`.
"""

import rules

from apps.accounts.roles import has_author_role, has_editor_role


@rules.predicate
def is_post_author(user, post) -> bool:
    return post is not None and post.author_id == user.pk


@rules.predicate
def is_published(user, post) -> bool:
    return post is not None and post.is_published


can_add_post = has_author_role | has_editor_role
can_change_post = (has_author_role & is_post_author) | has_editor_role
can_view_post = is_published | can_change_post
