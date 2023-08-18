from django import forms


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        placeholder = kwargs.pop("placeholder", "Buscar...")
        super().__init__(*args, **kwargs)
        self.fields["q"].widget.attrs.update({"placeholder": placeholder})

    q = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(),
    )
