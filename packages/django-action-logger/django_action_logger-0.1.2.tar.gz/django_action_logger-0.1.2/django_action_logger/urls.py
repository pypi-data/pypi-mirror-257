from django.urls import path

from . import views

app_name = "django_action_log"

urlpatterns = [
    path(
        "log",
        views.Log.as_view(),
        name="djangoactionlog",
    ),
]
