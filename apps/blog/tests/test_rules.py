"""
Tabela de autorização do blog.

Cada linha diz: este usuário, nesta situação, pode (ou não) fazer isto.
Ao mudar uma regra em apps/blog/rules.py, esta tabela precisa mudar junto.
"""

import pytest
from django.contrib.auth.models import AnonymousUser

from apps.accounts.roles import Role, revoke_role
from apps.blog.models import Post
from apps.blog.tests.factories import PostFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def users(reader, author, other_author, editor, superuser):
    return {
        "anonymous": AnonymousUser(),
        "reader": reader,
        "author": author,
        "other_author": other_author,
        "editor": editor,
        "superuser": superuser,
    }


@pytest.mark.parametrize(
    ("user", "allowed"),
    [
        ("anonymous", False),
        ("reader", False),
        ("author", True),
        ("other_author", True),
        ("editor", True),
        ("superuser", True),
    ],
)
def test_add_post(users, user, allowed):
    assert users[user].has_perm("blog.add_post") is allowed


@pytest.mark.parametrize("perm", ["blog.change_post", "blog.delete_post"])
@pytest.mark.parametrize(
    ("user", "allowed"),
    [
        ("anonymous", False),
        ("reader", False),
        ("author", True),
        ("other_author", False),
        ("editor", True),
        ("superuser", True),
    ],
)
def test_change_and_delete_post(users, user, allowed, perm):
    post = PostFactory(author=users["author"])
    assert users[user].has_perm(perm, post) is allowed


def test_author_who_lost_the_role_can_no_longer_change_own_post(author):
    post = PostFactory(author=author)
    revoke_role(author, Role.AUTHOR)
    fresh_author = type(author).objects.get(pk=author.pk)  # sem cache de grupos
    assert not fresh_author.has_perm("blog.change_post", post)


@pytest.mark.parametrize(
    ("user", "published_allowed", "draft_allowed"),
    [
        ("anonymous", True, False),
        ("reader", True, False),
        ("author", True, True),
        ("other_author", True, False),
        ("editor", True, True),
        ("superuser", True, True),
    ],
)
def test_view_post(users, user, published_allowed, draft_allowed):
    published = PostFactory(author=users["author"], status=Post.Status.PUBLISHED)
    draft = PostFactory(author=users["author"], status=Post.Status.DRAFT)
    assert users[user].has_perm("blog.view_post", published) is published_allowed
    assert users[user].has_perm("blog.view_post", draft) is draft_allowed
