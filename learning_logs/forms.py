from django import forms

from . import models


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        placeholder = kwargs.pop("placeholder", "Buscar...")
        super().__init__(*args, **kwargs)
        self.fields["q"].widget.attrs.update({"placeholder": placeholder})

    q = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(),
        required=False,
    )


class TopicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.pk = kwargs.pop("pk", None)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data["title"]
        if (
            models.Topic.objects.filter(title__iexact=title, owner=self.user)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise forms.ValidationError("Você já possui um tópico com esse título!")
        return title

    class Meta:
        model = models.Topic
        fields = ("title", "public")
        labels = {"title": "Título", "public": "Tornar tópico público?"}
        widgets = {"title": forms.TextInput(attrs={"autofocus": True})}


class EntryForm(forms.ModelForm):
    class Meta:
        model = models.Entry
        fields = ("content",)
        labels = {"content": "O que você aprendeu?"}
        widgets = {
            "content": forms.Textarea(attrs={"rows": 10, "cols": 50, "autofocus": True})
        }
