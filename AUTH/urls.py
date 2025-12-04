from django.urls import path
from .views import RegisterView, ProtectedView, LoginView, LogoutView, UpdateScoreView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("protected/", ProtectedView.as_view()),
    path("update-score/", UpdateScoreView.as_view()),
]