from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = "core"

urlpatterns = [
    path("", views.login, name="login"),
    path("login", views.login, name="login"),
    path("dashboard")
]
