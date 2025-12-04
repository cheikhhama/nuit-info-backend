from django.db import models
from django.contrib.auth.models import User

# --- Profile utilisateur ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    level = models.PositiveSmallIntegerField(default=1)  # niveau de l'utilisateur

    def __str__(self):
        return self.user.username

    def ajouter_score(self):
        """Ajoute des points selon le niveau"""
        if self.level == 1:
            self.score += 5
        elif self.level == 2:
            self.score += 10
        elif self.level == 3:
            self.score += 14
        self.save()


# --- Categorie ---
class Categorie(models.Model):
    nom = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom


# --- Base pour Information et Quiz ---
class ContenuBase(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField(blank=True, null=True)
    solution = models.TextField(blank=True, null=True)
    # on met related_name='+' pour ne pas créer de relation inverse par défaut
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='+')

    class Meta:
        abstract = True

    def __str__(self):
        return self.titre


# --- Information ---
class Information(ContenuBase):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='informations')


# --- Quiz ---
class Quiz(ContenuBase):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='quizzes')
    nom = models.CharField(max_length=200, blank=True, null=True)  # <-- ajouté
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self):
        if self.nom:
            return f"{self.nom} - {self.titre}"
        return self.titre

    def get_options(self):
        return [
            {
                "id": r.id,
                "label": r.texte,
                "isCorrect": r.est_correct
            }
            for r in self.reponses.all()
        ]




# --- Reponse ---
class Reponse(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='reponses')
    texte = models.CharField(max_length=400)
    est_correct = models.BooleanField(default=False)
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Réponse"
        verbose_name_plural = "Réponses"
        ordering = ['ordre']

    def __str__(self):
        return f"{self.texte} ({'✓' if self.est_correct else '✗'})"
