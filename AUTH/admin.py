from django.contrib import admin
from .models import Profile, Categorie, Information, Quiz, Reponse

# --- Profile ---
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'level')
    search_fields = ('user__username',)
    list_filter = ('level',)


# --- Categorie ---
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)


# --- Information ---
@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie')
    search_fields = ('titre', 'contenu')
    list_filter = ('categorie',)


# --- Reponse inline pour Quiz ---
class ReponseInline(admin.TabularInline):
    model = Reponse
    extra = 0  # pas de lignes inutiles
    max_num = 3
    min_num = 3

    # Forcer 3 réponses obligatoires en TabularInline
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.max_num = 3
        formset.min_num = 3
        formset.validate_max = True
        formset.validate_min = True
        return formset


# --- Quiz ---
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'created_at', 'updated_at')
    search_fields = ('titre', 'contenu')  # nom supprimé (n’existe pas dans ton modèle)
    list_filter = ('categorie', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ReponseInline]
