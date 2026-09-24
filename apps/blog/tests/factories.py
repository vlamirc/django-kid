import factory

from apps.accounts.tests.factories import UserFactory
from apps.blog.models import Post


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: f"Post número {n}")
    body = factory.Faker("paragraph", locale="pt_BR")
    author = factory.SubFactory(UserFactory)
    status = Post.Status.PUBLISHED
