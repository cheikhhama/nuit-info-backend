from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer

# ---------------------------
# Register View
# ---------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)

        except Exception as e:
            return Response(
                {"error": "Registration failed", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

# ---------------------------
# Protected View
# ---------------------------
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            return Response({"message": f"You are authenticated as {request.user.username}"})
        except Exception as e:
            return Response(
                {"error": "Unexpected error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ---------------------------
# Login View
# ---------------------------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Login failed", },
                status=status.HTTP_400_BAD_REQUEST
            )

# ---------------------------
# Logout View
# ---------------------------
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = LogoutSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Logout failed", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz
from .serializers import QuizSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from .models import Quiz, Categorie
from .serializers import QuizSerializer

class QuizListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        quizzes = Quiz.objects.all()
        categorie_id = request.GET.get('categorie')
        if categorie_id:
            quizzes = quizzes.filter(categorie__id=categorie_id)
        paginator = LimitOffsetPagination()
        paginator.default_limit = 2  # nombre d'éléments par page
        paginator.max_limit = 4      # limite maximale
        result_page = paginator.paginate_queryset(quizzes, request)
        serializer = QuizSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class QuizDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_200_OK)
   

from rest_framework import generics
from django.db.models import Count
from .models import Categorie
from .serializers import CategorieWithQuizCountSerializer

class CategorieWithQuizCountListAPIView(generics.ListAPIView):
    serializer_class = CategorieWithQuizCountSerializer

    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de quizzes
        return Categorie.objects.annotate(quiz_count=Count('quizzes'))


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Reponse, Profile
from .serializers import ReponseCheckSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Reponse, Profile
from .serializers import ReponseCheckSerializer

class VerifierReponseAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # ✅ JWT ou session auth
    def post(self, request, *args, **kwargs):
        serializer = ReponseCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reponse_id = serializer.validated_data['reponse_id']

        # Récupérer la réponse
        try:
            reponse = Reponse.objects.get(id=reponse_id)
        except Reponse.DoesNotExist:
            return Response({"error": "Réponse non trouvée"}, status=status.HTTP_404_NOT_FOUND)

        # Récupérer le profil de l'utilisateur
        profile, created = Profile.objects.get_or_create(user=request.user)

        # Vérification correcte/faux
        est_correct = reponse.est_correct

        # Calcul du score selon le niveau
        if est_correct:
            if profile.level == 1:
                profile.score += 5
            elif profile.level == 2:
                profile.score += 10
            elif profile.level == 3:
                profile.score += 14
        else:
            if profile.level == 1:
                profile.score = max(profile.score - 2, 0)
            elif profile.level == 2:
                profile.score = max(profile.score - 4, 0)
            elif profile.level == 3:
                profile.score = max(profile.score - 6, 0)

        profile.save()

        return Response({
            "quiz_id": reponse.quiz.id,
            "reponse_id": reponse.id,
            "est_correct": est_correct,
            "score": profile.score,
            "level": profile.level
        }, status=status.HTTP_200_OK)


