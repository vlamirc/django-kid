from django.urls import path

from apps.blog import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("meus-posts/", views.MyPostListView.as_view(), name="my_posts"),
    path("posts/novo/", views.PostCreateView.as_view(), name="post_create"),
    path("posts/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<slug:slug>/editar/", views.PostUpdateView.as_view(), name="post_update"),
    path("posts/<slug:slug>/excluir/", views.PostDeleteView.as_view(), name="post_delete"),
]
