import factory
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model

DEFAULT_PASSWORD = "uma-senha-bem-forte-42"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"usuario{n}")
    email = factory.LazyAttribute(lambda user: f"{user.username}@example.com")
    password = factory.django.Password(DEFAULT_PASSWORD)

    @factory.post_generation
    def verified_email(user, create, extracted, **kwargs):
        if create:
            EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)
