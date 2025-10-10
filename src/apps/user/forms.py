from django import forms


class ConnexionForm(forms.Form):
    username = forms.CharField(
        label="Nom de login ",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "fieldset border"}),
    )
    password = forms.CharField(
        label="Mot de passe ",
        widget=forms.PasswordInput(attrs={"class": "fieldset border"}),
    )

    class Meta:
        widgets = {}
