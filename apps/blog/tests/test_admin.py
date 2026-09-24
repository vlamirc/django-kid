import pytest
from django.urls import reverse

from apps.blog.tests.factories import PostFactory

pytestmark = pytest.mark.django_db


def test_superuser_sees_posts_in_admin(client, superuser):
    PostFactory(title="Post no admin")
    client.force_login(superuser)
    response = client.get(reverse("admin:blog_post_changelist"))
    assert response.status_code == 200
    assert "Post no admin" in response.content.decode()
