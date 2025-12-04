from django.urls import path
from .views import RegisterView, ProtectedView, LoginView, LogoutView,QuizListAPIView,QuizDetailAPIView,CategorieWithQuizCountListAPIView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("protected/", ProtectedView.as_view()),
    path('quizzes/', QuizListAPIView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', QuizDetailAPIView.as_view(), name='quiz-detail'),
    path('categories-count/', CategorieWithQuizCountListAPIView.as_view(), name='categories-count'),

]