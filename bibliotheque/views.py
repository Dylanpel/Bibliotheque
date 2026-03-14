from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

import json
from datetime import date
from urllib.parse import urlencode
from urllib.request import urlopen

from .models import Auteur, Livre, Categorie, Edition

class IndexViews(generic.ListView): 
    context_object_name = "livres"
    model = Livre
    def get_queryset(self):
        return Livre.objects.order_by("-id")[:5]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["auteur"] = Auteur.objects.all().order_by("-nom")[:5]
        context["edition"] = Edition.objects.all().order_by("-libelle")[:5]
        return context

class ListeLivre(generic.ListView):
    model = Livre
    template_name = "bibliotheque/liste-livre.html"
    context_object_name = "livres"
    def get_queryset(self):
        order = self.request.GET.get('order', 'asc')
        if order == 'asc':
             return Livre.objects.order_by("id")
        else :
             return Livre.objects.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.request.GET.get('order', 'asc')
        return context

class DetailView(generic.DetailView):
    model = Livre
    template_name = "bibliotheque/detail.html"

class ScanIsbn(generic.TemplateView):
    template_name = "bibliotheque/form_isbn.html"

    def post(self, request, *args, **kwargs):
        isbn = request.POST.get("isbn")
        
        return redirect(f"/ajouter?isbn={isbn}")


class LivreCreate(CreateView):
    model = Livre
    template_name = "bibliotheque/ajouter.html"
    fields = "__all__"

    def get_initial(self):
        initial = super().get_initial()
        isbn = self.request.GET.get("isbn")
        query = urlencode({"q": f"isbn:{isbn}"})
        url = f"https://www.googleapis.com/books/v1/volumes?{query}"

        with urlopen(url, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))

        if not payload.get("items"):
            return initial

        info = payload["items"][0]["volumeInfo"]

        initial["titre"] = info.get("title", "")
        initial["description"] = info.get("description", "")
        initial["date_parution"] = info.get("publishedDate", "")
        initial["isbn"] = isbn

        publisher = info.get("publisher")
        if publisher:
            if Edition.objects.filter(libelle=publisher).count() == 0:
                Edition.objects.create(libelle=publisher)

        for auteur in info.get("authors", []):
            if Auteur.objects.filter(nom=auteur).count() == 0:
                Auteur.objects.create(nom=auteur)

        return initial

class LivreDelete(DeleteView):
    model = Livre
    success_url = "/"

class LivreUpdate(UpdateView):
    model = Livre
    template_name = "bibliotheque/update.html"
    fields = "__all__"
    success_url = "/"