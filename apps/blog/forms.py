from django import forms

from apps.blog.models import Post
from apps.core.forms import BootstrapFormMixin


class PostForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "subtitle", "body", "status"]
        widgets = {"body": forms.Textarea(attrs={"rows": 14})}
        help_texts = {"body": "Texto simples. Parágrafos são separados por uma linha em branco."}
