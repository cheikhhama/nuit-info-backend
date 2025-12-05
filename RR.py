import os
import django
import random

# --- Initialisation Django ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from AUTH.models import Categorie, Quiz, Reponse, Information, Profile
from django.contrib.auth.models import User

# --- Texte de base ---
base_contenu = """
À l’heure où la fin du support de Windows 10 met en évidence la dépendance structurelle aux Big Tech,
les établissements scolaires se retrouvent confrontés à un empire numérique puissant : matériel rendu
obsolète alors qu’il fonctionne encore, licences coûteuses, stockage de données hors UE, écosystèmes fermés,
abonnements indispensables…

Face à ce Goliath numérique, l’École peut devenir un village résistant, ingénieux, autonome et créatif, à
l’image du célèbre village d’Astérix.

C’est précisément l’ambition de la démarche NIRD : permettre aux établissements scolaires d’adopter
progressivement un Numérique Inclusif, Responsable et Durable, en redonnant du pouvoir d’agir aux équipes
éducatives et en renforçant leur autonomie technologique.

Votre équipe est engagée pour créer une application Web qui aide le public — élèves, enseignants, familles,
collectivités — à comprendre comment un établissement peut réduire ses dépendances numériques et entrer
dans la démarche NIRD de manière progressive, réaliste et motivante.
"""

# --- Catégories NIRD ---
categories_nird = [
    "Éducation Numérique",
    "Bien-être Numérique",
    "Gestion du temps d'écran",
    "Sécurité et confidentialité",
    "Engagement citoyen"
]

# --- Questions plausibles pour 100 entrées ---
questions_templates = [
    {
        "question": "Quelle pratique aide les élèves à réduire leur dépendance aux écrans ?",
        "options": ["Fixer des horaires d'utilisation", "Augmenter le temps d'écran", "Ignorer le problème"],
        "answer": "Fixer des horaires d'utilisation"
    },
    {
        "question": "Quel rôle peut jouer un enseignant dans la démarche NIRD ?",
        "options": ["Sensibiliser et guider", "Encourager l’usage illimité", "Ne rien changer"],
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
    },
    {
        "question": "Comment réduire l’obsolescence du matériel informatique ?",
        "options": ["Réparer et réutiliser", "Changer chaque année", "Ignorer le matériel obsolète"],
        "answer": "Réparer et réutiliser"
    },
    {
        "question": "Quelle stratégie implique les familles dans le numérique responsable ?",
        "options": ["Organiser des ateliers et informer", "Ne pas communiquer", "Imposer des règles strictes sans dialogue"],
        "answer": "Organiser des ateliers et informer"
    },
    {
        "question": "Comment un établissement peut-il limiter l’usage excessif des licences payantes ?",
        "options": ["Privilégier les logiciels libres", "Acheter toujours plus de licences", "Ignorer les licences"],
        "answer": "Privilégier les logiciels libres"
    },
    {
        "question": "Quelle pratique favorise le bien-être numérique des élèves ?",
        "options": ["Ateliers hors écran", "Augmenter le temps d’écran", "Surveillance stricte"], 
        "answer": "Ateliers hors écran"
    },
    {
        "question": "Comment renforcer la sécurité des données ?",
        "options": ["Stocker les données localement ou en UE", "Tout mettre sur le cloud étranger", "Ignorer la sécurité"], 
        "answer": "Stocker les données localement ou en UE"
    }
]

# --- Fonctions utilitaires ---
def create_categories():
    categories = []
    for cat_name in categories_nird:
        cat, _ = Categorie.objects.get_or_create(nom=cat_name)
        categories.append(cat)
    return categories

def create_users(n=5):
    users = []
    for i in range(1, n+1):
        user, _ = User.objects.get_or_create(username=f"user{i}")
        Profile.objects.get_or_create(user=user)
        users.append(user)
    return users

def create_quiz(category, template, index):
    quiz = Quiz.objects.create(
        titre=f"Quiz NIRD {index} : {template['question']}",
        contenu=base_contenu,
        categorie=category
    )
    options = template["options"].copy()
    random.shuffle(options)
    for ordre, texte in enumerate(options, 1):
        Reponse.objects.create(
            quiz=quiz,
            texte=texte,
            est_correct=(texte == template["answer"]),
            ordre=ordre
        )
    return quiz

def create_information(category, index):
    titre = f"Information NIRD {index} - {category.nom}"
    contenu = (
        f"{base_contenu}\n\n"
        f"Conseil pratique #{index} pour {category.nom} : adopter des méthodes responsables et durables pour réduire la dépendance numérique."
    )
    return Information.objects.create(titre=titre, contenu=contenu, categorie=category)

# --- SCRIPT PRINCIPAL ---
def populate_nird(n=100):
    categories = create_categories()
    create_users(n=5)

    for i in range(1, n+1):
        category = random.choice(categories)
        template = random.choice(questions_templates)
        create_quiz(category, template, i)
        create_information(category, i)

    print(f"✅ Base remplie avec {n} quizzes et {n} informations NIRD.")

if __name__ == "__main__":
    populate_nird()
