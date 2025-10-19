from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label="",
        widget=forms.FileInput(attrs={"class": "file-input"}),
    )


class UploadURL(forms.Form):
    url = forms.URLField(
        label="Copier-coller le lien ici :",
        widget=forms.URLInput(attrs={"class": "input"}),
    )
