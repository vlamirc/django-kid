from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from rules.contrib.views import PermissionRequiredMixin

from apps.blog.forms import PostForm
from apps.blog.models import Post


class PostListView(generic.ListView):
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.published().select_related("author")


class PostDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Post
    permission_required = "blog.view_post"
    queryset = Post.objects.select_related("author")
    template_name = "blog/post_detail.html"


class MyPostListView(PermissionRequiredMixin, generic.ListView):
    permission_required = "blog.add_post"
    template_name = "blog/my_post_list.html"
    context_object_name = "posts"
    paginate_by = 20

    def get_queryset(self):
        return Post.objects.by_author(self.request.user).order_by("-created_at")


class PostCreateView(PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    permission_required = "blog.add_post"
    template_name = "blog/post_form.html"
    success_message = "Post criado."

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(PermissionRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    permission_required = "blog.change_post"
    template_name = "blog/post_form.html"
    success_message = "Post atualizado."


class PostDeleteView(PermissionRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Post
    permission_required = "blog.delete_post"
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:my_posts")
    success_message = "Post excluído."
