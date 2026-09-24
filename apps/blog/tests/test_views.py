import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertRedirects

from apps.blog.models import Post
from apps.blog.tests.factories import PostFactory

pytestmark = pytest.mark.django_db


def login_url(next_url):
    return f"{reverse('account_login')}?next={next_url}"


class TestPostList:
    url = reverse("blog:post_list")

    def test_shows_published_posts_only(self, client):
        PostFactory(title="Post publicado")
        PostFactory(title="Post em rascunho", status=Post.Status.DRAFT)
        response = client.get(self.url)
        assertContains(response, "Post publicado")
        assertNotContains(response, "Post em rascunho")

    def test_shows_a_message_when_empty(self, client):
        assertContains(client.get(self.url), "Nenhum post publicado ainda.")

    def test_is_paginated(self, client):
        PostFactory.create_batch(11)
        response = client.get(self.url)
        assert len(response.context["posts"]) == 10
        assertContains(response, "Posts anteriores")
        assert len(client.get(self.url, {"page": 2}).context["posts"]) == 1

    def test_uses_a_fixed_number_of_queries(self, client, django_assert_num_queries):
        PostFactory.create_batch(5)
        with django_assert_num_queries(2):  # contagem para paginação + posts com autores
            client.get(self.url)

    def test_menu_offers_writing_only_to_those_who_can_write(self, client, reader, author):
        client.force_login(reader)
        assertNotContains(client.get(self.url), "Escrever")
        client.force_login(author)
        assertContains(client.get(self.url), "Escrever")


class TestPostDetail:
    def test_anyone_can_read_a_published_post(self, client):
        post = PostFactory(title="Leia-me", body="Primeiro parágrafo.\n\nSegundo.")
        response = client.get(post.get_absolute_url())
        assertContains(response, "Leia-me")
        assertContains(response, "<p>Primeiro parágrafo.</p>", html=True)

    def test_post_body_is_escaped(self, client):
        post = PostFactory(body="<script>alert(1)</script>")
        assertNotContains(client.get(post.get_absolute_url()), "<script>alert(1)</script>")

    def test_anonymous_is_sent_to_login_for_a_draft(self, client):
        post = PostFactory(status=Post.Status.DRAFT)
        url = post.get_absolute_url()
        assertRedirects(client.get(url), login_url(url), fetch_redirect_response=False)

    def test_reader_cannot_see_a_draft(self, client, reader):
        client.force_login(reader)
        response = client.get(PostFactory(status=Post.Status.DRAFT).get_absolute_url())
        assert response.status_code == 403

    def test_author_sees_own_draft_with_edit_buttons(self, client, author):
        client.force_login(author)
        post = PostFactory(author=author, status=Post.Status.DRAFT)
        response = client.get(post.get_absolute_url())
        assertContains(response, "Rascunho")
        assertContains(response, reverse("blog:post_update", args=[post.slug]))

    def test_other_users_see_no_edit_buttons(self, client, reader):
        client.force_login(reader)
        post = PostFactory()
        assertNotContains(
            client.get(post.get_absolute_url()), reverse("blog:post_update", args=[post.slug])
        )

    def test_unknown_post_is_404(self, client):
        response = client.get(reverse("blog:post_detail", args=["nao-existe"]))
        assert response.status_code == 404
        assertContains(response, "Página não encontrada", status_code=404)


class TestMyPosts:
    url = reverse("blog:my_posts")

    def test_lists_only_own_posts_including_drafts(self, client, author, other_author):
        PostFactory(author=author, title="Meu rascunho", status=Post.Status.DRAFT)
        PostFactory(author=other_author, title="Post de outra pessoa")
        client.force_login(author)
        response = client.get(self.url)
        assertContains(response, "Meu rascunho")
        assertNotContains(response, "Post de outra pessoa")

    def test_reader_is_forbidden(self, client, reader):
        client.force_login(reader)
        assert client.get(self.url).status_code == 403


class TestPostCreate:
    url = reverse("blog:post_create")
    data = {"title": "Novo post", "subtitle": "", "body": "Texto.", "status": "published"}

    def test_anonymous_is_sent_to_login(self, client):
        assertRedirects(client.get(self.url), login_url(self.url), fetch_redirect_response=False)

    def test_reader_is_forbidden(self, client, reader):
        client.force_login(reader)
        response = client.get(self.url)
        assert response.status_code == 403
        assertContains(response, "Acesso negado", status_code=403)

    def test_author_creates_a_post_signed_by_them(self, client, author):
        client.force_login(author)
        response = client.post(self.url, self.data, follow=True)
        post = Post.objects.get()
        assert post.author == author
        assertRedirects(response, post.get_absolute_url())
        assertContains(response, "Post criado.")

    def test_invalid_form_shows_errors(self, client, author):
        client.force_login(author)
        response = client.post(self.url, {**self.data, "title": ""})
        assertContains(response, "Este campo é obrigatório.")
        assert not Post.objects.exists()


class TestPostUpdate:
    def url(self, post):
        return reverse("blog:post_update", args=[post.slug])

    def test_owner_updates_their_post(self, client, author):
        post = PostFactory(author=author)
        client.force_login(author)
        response = client.post(
            self.url(post), {"title": "Novo título", "body": "Novo texto.", "status": "draft"}
        )
        post.refresh_from_db()
        assert (post.title, post.status) == ("Novo título", Post.Status.DRAFT)
        assertRedirects(response, post.get_absolute_url(), fetch_redirect_response=False)

    def test_other_author_is_forbidden(self, client, other_author):
        client.force_login(other_author)
        assert client.get(self.url(PostFactory())).status_code == 403

    def test_editor_can_edit_any_post(self, client, editor):
        client.force_login(editor)
        response = client.get(self.url(PostFactory()))
        assertContains(response, "Editar post")


class TestPostDelete:
    def url(self, post):
        return reverse("blog:post_delete", args=[post.slug])

    def test_owner_deletes_their_post(self, client, author):
        post = PostFactory(author=author)
        client.force_login(author)
        assertContains(client.get(self.url(post)), "Tem certeza")
        response = client.post(self.url(post))
        assertRedirects(response, reverse("blog:my_posts"))
        assert not Post.objects.exists()

    def test_other_author_is_forbidden(self, client, other_author):
        post = PostFactory()
        client.force_login(other_author)
        assert client.post(self.url(post)).status_code == 403
        assert Post.objects.filter(pk=post.pk).exists()
