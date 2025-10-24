from django import forms
from .models import LLMModel, Prompt


class LLMModelForm(forms.ModelForm):
    class Meta:
        model = LLMModel
        fields = ["LLM", "temperature", "verbosity"]


class PromptForm(forms.ModelForm):
    class Meta:
        model = Prompt
        fields = ["name", "target", "prompt_text", "active"]
