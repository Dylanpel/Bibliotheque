from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import redirect

import json
from datetime import date
from urllib.parse import urlencode
from urllib.request import urlopen

from .models import Auteur, Livre, Categorie, Edition

class IndexViews(generic.ListView): 
    context_object_name = "livres"
    model = Livre

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
        
        print(payload["items"][0]["volumeInfo"]["title"])
        print(payload["items"][0]["volumeInfo"]["authors"])
        print(payload["items"][0]["volumeInfo"]["publisher"])
        print(payload["items"][0]["volumeInfo"]["publishedDate"])
        print(payload["items"][0]["volumeInfo"]["description"])

        initial["titre"] = payload["items"][0]["volumeInfo"]["title"]
        initial["description"] = payload["items"][0]["volumeInfo"]["description"]
        initial["date_parution"] = payload["items"][0]["volumeInfo"]["publishedDate"]

        edition = payload["items"][0]["volumeInfo"]["publisher"]
        if Edition.objects.filter(libelle=edition).count() == 0:
            Edition.objects.create(libelle=edition)


        for auteur in payload["items"][0]["volumeInfo"]["authors"]:
           if Auteur.objects.filter(nom=auteur).count() == 0:
               Auteur.objects.create(nom = auteur)
               
        initial["isbn"]= isbn
        return initial

class LivreDelete(DeleteView):
    model = Livre
    success_url = "/"

class LivreUpdate(UpdateView):
    model = Livre
    template_name = "bibliotheque/update.html"
    fields = "__all__"
    success_url = "/"