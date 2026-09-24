from apps.blog.forms import PostForm


def test_fields_use_bootstrap_classes():
    form = PostForm()
    assert form.fields["title"].widget.attrs["class"] == "form-control"
    assert form.fields["status"].widget.attrs["class"] == "form-select"


def test_author_is_not_editable_through_the_form():
    assert "author" not in PostForm().fields
