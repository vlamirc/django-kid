from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from rules.contrib.models import RulesModel

from apps.blog import rules as blog_rules


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=Post.Status.PUBLISHED)

    def by_author(self, user):
        return self.filter(author=user)


class Post(RulesModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Rascunho"
        PUBLISHED = "published", "Publicado"

    title = models.CharField("título", max_length=200)
    subtitle = models.CharField("subtítulo", max_length=200, blank=True)
    slug = models.SlugField("endereço", max_length=220, unique=True, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="autor",
        on_delete=models.PROTECT,
        related_name="posts",
    )
    body = models.TextField("texto")
    status = models.CharField("situação", max_length=20, choices=Status, default=Status.DRAFT)
    published_at = models.DateTimeField("publicado em", null=True, blank=True)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    objects = PostQuerySet.as_manager()

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ["-published_at", "-created_at"]
        indexes = [models.Index(fields=["status", "-published_at"])]
        rules_permissions = {
            "add": blog_rules.can_add_post,
            "view": blog_rules.can_view_post,
            "change": blog_rules.can_change_post,
            "delete": blog_rules.can_change_post,
        }

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    @property
    def is_published(self) -> bool:
        return self.status == self.Status.PUBLISHED

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._unique_slug()
        if self.is_published and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def _unique_slug(self) -> str:
        # O endereço é definido na criação e não muda, para não quebrar links.
        base = slugify(self.title)[:200] or "post"
        slug, suffix = base, 2
        while Post.objects.filter(slug=slug).exists():
            slug, suffix = f"{base}-{suffix}", suffix + 1
        return slug
