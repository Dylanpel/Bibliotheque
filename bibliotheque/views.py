from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Auteur, Livre, Categorie

class IndexViews(generic.ListView): 
    context_object_name = "livres"
    model = Livre

class DetailView(generic.DetailView):
    model = Livre
    template_name = "bibliotheque/detail.html"

class LivreCreate(CreateView):
    model = Livre
    template_name = "bibliotheque/ajouter.html"
    fields = "__all__"

class LivreDelete(DeleteView):
    model = Livre
    success_url = "/"

class LivreUpdate(UpdateView):
    model = Livre
    template_name = "bibliotheque/update.html"
    fields = "__all__"
    success_url = "/"