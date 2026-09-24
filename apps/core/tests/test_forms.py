from django import forms

from apps.core.forms import BootstrapFormMixin


class SampleForm(BootstrapFormMixin, forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "extra"}))
    kind = forms.ChoiceField(choices=[("a", "A")])
    agree = forms.BooleanField()


def test_each_widget_gets_the_right_bootstrap_class():
    form = SampleForm()
    assert form.fields["name"].widget.attrs["class"] == "extra form-control"
    assert form.fields["kind"].widget.attrs["class"] == "form-select"
    assert form.fields["agree"].widget.attrs["class"] == "form-check-input"
