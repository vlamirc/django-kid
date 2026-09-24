import pytest
from django.contrib.auth import get_user_model
from django.core.management import CommandError, call_command

from apps.blog.models import Post

pytestmark = pytest.mark.django_db


def test_creates_demo_users_and_posts():
    call_command("seed_demo")
    autor = get_user_model().objects.get(username="autor")
    assert autor.has_perm("blog.add_post")
    assert Post.objects.published().count() == 2
    assert Post.objects.count() == 3


def test_refuses_to_run_twice():
    call_command("seed_demo")
    with pytest.raises(CommandError):
        call_command("seed_demo")
