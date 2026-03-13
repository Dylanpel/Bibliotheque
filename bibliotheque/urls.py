from django.urls import path
from . import views

app_name = "bibliotheque"
urlpatterns = [
    # ex: /polls/
    path("", views.IndexViews.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="details"),
]