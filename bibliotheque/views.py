from django.shortcuts import render
from django.views import generic

from .models import Auteur, Livre, Categorie

class IndexViews(generic.ListView): 
    context_object_name = "livres"
    model = Livre

class DetailView(generic.DetailView):
    model = Livre
    template_name = "bibliotheque/detail.html"