from django.urls import path

from views import blockedView, indexView


urlpatterns = [
    path("", indexView),
    path("blocked/", blockedView),
]