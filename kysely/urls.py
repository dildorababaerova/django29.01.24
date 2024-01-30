from django.urls import path

from . import views

urlpatterns = [
    path("", views.indeksi, name="indeksi"),
    path("<int:question_id>/", views.näytä, name="näytä"),
    path("<int:question_id>/tulokset/", views.tulokset, name="tulokset"),
    path("<int:question_id>/äänestä/", views.äänestä, name="äänestä"),
]