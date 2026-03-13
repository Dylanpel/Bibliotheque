from django.urls import path
from . import views

app_name = "bibliotheque"
urlpatterns = [
    # ex: /polls/
    path("", views.IndexViews.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="details"),
    path("isbn", views.ScanIsbn.as_view(), name="isbn"),
    path("ajouter", views.LivreCreate.as_view(), name="ajouter"),
    path("<int:pk>/modifier", views.LivreUpdate.as_view(), name="modifier"),
    path("<int:pk>/supprimer", views.LivreDelete.as_view(), name="delete")
]