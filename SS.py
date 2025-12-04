import os
import django
import random

# --- Initialiser Django ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')  # remplace 'project'
django.setup()

from AUTH.models import Categorie, Quiz, Reponse, Information, Profile
from django.contrib.auth.models import User

# --- Données thématiques NIRD ---
categories_nird = [
    "Éducation Numérique",
    "Bien-être Numérique",
    "Gestion du temps d'écran",
    "Sécurité et confidentialité",
    "Engagement citoyen"
]

questions_templates = [
    {
        "question": "Quelle pratique aide les élèves à réduire leur dépendance aux écrans ?",
        "options": ["Fixer des horaires d'utilisation", "Augmenter le temps d'écran", "Ignorer le problème"],
        "answer": "Fixer des horaires d'utilisation"
    },
    {
        "question": "Quel rôle peut jouer un enseignant dans la démarche NIRD ?",
        "options": ["Sensibiliser et guider", "Encourager l'usage illimité", "Ne rien changer"],
        "answer": "Sensibiliser et guider"
    },
    {
        "question": "Quelle action aide un établissement à réduire la dépendance numérique ?",
        "options": ["Organiser des activités hors écran", "Supprimer toutes les technologies", "Ignorer les habitudes numériques"],
        "answer": "Organiser des activités hors écran"
    },
    {
        "question": "Comment impliquer les familles dans la démarche NIRD ?",
        "options": ["Communiquer et sensibiliser", "Interdire totalement les écrans à la maison", "Ne pas informer les parents"],
        "answer": "Communiquer et sensibiliser"
    },
    {
        "question": "Quel outil peut aider à mesurer la dépendance numérique ?",
        "options": ["Questionnaires et suivi des usages", "Suppression totale des appareils", "Ignorer les données"],
        "answer": "Questionnaires et suivi des usages"
    }
]

# --- Fonctions utilitaires ---
def create_categories():
    categories = []
    for cat_name in categories_nird:
        cat, created = Categorie.objects.get_or_create(nom=cat_name)
        categories.append(cat)
    return categories

def create_users(n=5):
    users = []
    for i in range(1, n+1):
        user, created = User.objects.get_or_create(username=f"user{i}")
        Profile.objects.get_or_create(user=user)
        users.append(user)
    return users

def create_quiz(category, template, index):
    quiz = Quiz.objects.create(
        titre=f"Quiz NIRD {index}: {template['question']}",
        contenu="Choisissez la bonne réponse pour progresser dans la démarche NIRD",
        categorie=category
    )

    # Mélanger les options
    options = template['options'].copy()
    random.shuffle(options)

    for ordre, texte in enumerate(options, 1):
        Reponse.objects.create(
            quiz=quiz,
            texte=texte,
            est_correct=(texte == template['answer']),
            ordre=ordre
        )
    return quiz

def create_information(category, index):
    titre = f"Information NIRD {index} - {category.nom}"
    contenu = f"Ceci est un conseil pratique pour réduire la dépendance numérique dans {category.nom}."
    info = Information.objects.create(titre=titre, contenu=contenu, categorie=category)
    return info

# --- SCRIPT PRINCIPAL ---
def populate_nird(n_quizzes=100):
    categories = create_categories()
    create_users(n=5)

    for i in range(1, n_quizzes + 1):
        category = random.choice(categories)
        template = random.choice(questions_templates)
        create_quiz(category, template, i)
        create_information(category, i)

    print(f"✅ Base de données remplie avec {n_quizzes} quizzes et informations NIRD.")

if __name__ == "__main__":
    populate_nird()
