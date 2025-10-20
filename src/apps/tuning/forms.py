from django import forms
from .models import LLMModel, Prompt


class LLMModelForm(forms.ModelForm):
    class Meta:
        model = LLMModel
        fields = ["LLM", "temperature", "verbosity"]
