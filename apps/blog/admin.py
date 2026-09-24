from django.contrib import admin
from rules.contrib.admin import ObjectPermissionsModelAdmin

from apps.blog.models import Post


@admin.register(Post)
class PostAdmin(ObjectPermissionsModelAdmin):
    list_display = ("title", "author", "status", "published_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("title", "body")
    readonly_fields = ("slug", "created_at", "updated_at")
    list_select_related = ("author",)
    date_hierarchy = "published_at"
