import pytest
from django.utils import timezone

from apps.blog.models import Post
from apps.blog.tests.factories import PostFactory

pytestmark = pytest.mark.django_db


class TestSlug:
    def test_is_generated_from_title(self):
        post = PostFactory(title="Olá, Mundo do Django!")
        assert post.slug == "ola-mundo-do-django"

    def test_gets_a_suffix_when_title_repeats(self):
        first = PostFactory(title="Mesmo título")
        second = PostFactory(title="Mesmo título")
        third = PostFactory(title="Mesmo título")
        assert [first.slug, second.slug, third.slug] == [
            "mesmo-titulo",
            "mesmo-titulo-2",
            "mesmo-titulo-3",
        ]

    def test_does_not_change_when_title_changes(self):
        post = PostFactory(title="Título original")
        post.title = "Título novo"
        post.save()
        post.refresh_from_db()
        assert post.slug == "titulo-original"

    def test_falls_back_when_title_has_no_letters(self):
        assert PostFactory(title="!!!").slug == "post"


class TestPublishing:
    def test_draft_has_no_publication_date(self):
        assert PostFactory(status=Post.Status.DRAFT).published_at is None

    def test_publishing_sets_the_publication_date(self):
        post = PostFactory(status=Post.Status.DRAFT)
        post.status = Post.Status.PUBLISHED
        post.save()
        assert post.published_at is not None
        assert post.is_published

    def test_saving_again_keeps_the_original_publication_date(self):
        post = PostFactory(status=Post.Status.PUBLISHED)
        original = post.published_at
        post.title = "Editado"
        post.save()
        assert post.published_at == original

    def test_explicit_publication_date_is_kept(self):
        date = timezone.now() - timezone.timedelta(days=3)
        assert PostFactory(published_at=date).published_at == date


class TestQuerySet:
    def test_published_excludes_drafts(self):
        published = PostFactory(status=Post.Status.PUBLISHED)
        PostFactory(status=Post.Status.DRAFT)
        assert list(Post.objects.published()) == [published]

    def test_by_author_returns_only_their_posts(self):
        mine = PostFactory()
        PostFactory()
        assert list(Post.objects.by_author(mine.author)) == [mine]

    def test_newest_first(self):
        old = PostFactory(published_at=timezone.now() - timezone.timedelta(days=1))
        new = PostFactory()
        assert list(Post.objects.all()) == [new, old]


def test_str_is_the_title():
    assert str(PostFactory.build(title="Meu post")) == "Meu post"


def test_absolute_url_uses_the_slug():
    assert PostFactory(title="Um post").get_absolute_url() == "/posts/um-post/"
