from django.db import models
from django.urls import reverse


class Auteur(models.Model):
    nom = models.CharField(max_length=255)
    def __str__(self):
        return self.nom

class Categorie(models.Model):
    libelle = models.CharField(max_length=250)
    def __str__(self):
        return self.libelle
    
class Edition(models.Model):
    libelle = models.CharField(max_length=200)
    def __str__(self):
        return self.libelle

class Livre(models.Model):
    titre = models.CharField(max_length=250)
    description = models.TextField()
    date_parution = models.PositiveIntegerField("Date de Parution")
    isbn = models.CharField(max_length=20)
    auteur = models.ManyToManyField(Auteur)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('bibliotheque:details', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.titre