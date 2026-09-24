from allauth.account.decorators import secure_admin_login
from django.contrib import admin
from django.urls import include, path

from apps.core.views import healthz

# O login do admin passa pelo allauth, então também exige 2FA quando ativo.
admin.site.login = secure_admin_login(admin.site.login)
admin.site.site_header = "Django Kid - Administração"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("contas/", include("allauth.urls")),
    path("healthz/", healthz, name="healthz"),
    path("", include("apps.blog.urls")),
]
