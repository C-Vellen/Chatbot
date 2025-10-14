from django.urls import re_path
from . import views
from . import apps

# from .views import GenerateView

app_name = apps.ChatConfig.name

urlpatterns = [
    re_path(r"^summarize/$", views.summarize_text, name="summarize"),
    re_path(r"^chat/$", views.chat, name="chat"),
    re_path(r"^answer/$", views.answer),
    re_path(r"^talk/$", views.talk, name="talk"),
    re_path(r"^update/$", views.update),
]
