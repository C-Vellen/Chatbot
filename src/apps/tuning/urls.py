from django.urls import re_path
from . import views
from . import apps

# from .views import GenerateView

app_name = apps.TuningConfig.name

urlpatterns = [
    re_path(r"^$", views.model_tuning, name="model_tuning"),
    re_path(r"^prompt/$", views.prompt_tuning, name="prompt_tuning"),
]
