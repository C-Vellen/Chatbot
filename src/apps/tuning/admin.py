from django.contrib import admin
from .models import LLMModel, Prompt


@admin.register(LLMModel)
class LLMModelAdmin(admin.ModelAdmin):

    # affichage des libellés
    list_display = ["id", "LLM", "temperature", "verbosity", "active"]


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):

    # affichage des libellés
    list_display = ["id", "name", "target", "prompt_text", "active"]
