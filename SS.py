import os
import django
import random

# --- Initialiser Django ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')  # à adapter selon ton projet
django.setup()

from AUTH.models import Categorie, Information

# --- Catégories NIRD ---
categories_nird = [
    "Éducation Numérique",
    "Bien-être Numérique",
    "Gestion du temps d'écran",
    "Sécurité et confidentialité",
    "Engagement citoyen"
]

# --- Exemples de contenus et solutions ---
contenus_textes = [
    "Ce conseil aide à réduire la dépendance numérique en classe.",
    "Encouragez les activités hors écran pour équilibrer le temps d'écran.",
    "Sensibilisez les élèves aux risques liés à l'utilisation excessive des écrans.",
    "Impliquez les familles dans la gestion du temps d'écran à la maison.",
    "Utilisez des questionnaires pour mesurer la dépendance numérique.",
    "Organisez des ateliers sur le bien-être numérique.",
    "Favorisez l'utilisation responsable des outils numériques.",
    "Proposez des temps d'activités créatives sans technologie.",
    "Informez les enseignants des bonnes pratiques NIRD.",
    "Créez des espaces dédiés aux pauses numériques."
]

solutions_textes = [
    "Planifier des temps sans écran chaque jour.",
    "Mettre en place un suivi des usages numériques.",
    "Organiser des activités collaboratives hors écran.",
    "Sensibiliser les parents aux bonnes pratiques numériques.",
    "Créer des ateliers ludiques pour les élèves sur le bien-être numérique.",
    "Utiliser des outils de mesure et feedback pour les élèves.",
    "Limiter l'accès aux applications distrayantes pendant les cours.",
    "Encourager la participation à des activités sportives et artistiques.",
    "Mettre en place des règles claires sur l'utilisation des écrans.",
    "Valoriser les moments de déconnexion pour toute la communauté éducative."
]

# --- Fonctions utilitaires ---
def create_categories():
    categories = []
    for cat_name in categories_nird:
        cat, created = Categorie.objects.get_or_create(nom=cat_name)
        categories.append(cat)
    return categories

def create_informations(categories, n=100):
    for i in range(1, n+1):
        category = random.choice(categories)
        contenu = random.choice(contenus_textes)
        solution = random.choice(solutions_textes)
        titre = f"Information NIRD {i} - {category.nom}"

        Information.objects.create(
            titre=titre,
            contenu=contenu,
            solution=solution,
            categorie=category
        )

# --- SCRIPT PRINCIPAL ---
if __name__ == "__main__":
    categories = create_categories()
    create_informations(categories, n=100)
    print("✅ 100 informations NIRD avec solutions insérées avec succès !")
