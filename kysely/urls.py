from django.urls import path

from . import views

app_name = "kysely"
urlpatterns = [
    path("", views.ListaNäkymä.as_view(), name="indeksi"),
    path("<int:pk>/", views.NäytäNäkymä.as_view(), name="näytä"),
    path("<int:pk>/tulokset/", views.TuloksetNäkymä.as_view(), name="tulokset"),
    path("<int:kysymys_id>/äänestä/", views.äänestä, name="äänestä"),
]