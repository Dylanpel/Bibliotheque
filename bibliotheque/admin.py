from django.contrib import admin

from .models import Auteur, Livre, Categorie, Edition

admin.site.register(Auteur)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ["titre","get_auteur", "date_parution", "categorie"]
    list_filter = ["titre"]
    search_fields = ["titre"]
    def get_auteur(self, obj):
        return ([f"{a.nom}" for a in obj.auteur.all()])
    get_auteur.short_description = "auteur"
admin.site.register(Livre, QuestionAdmin)
admin.site.register(Categorie)
admin.site.register(Edition)
