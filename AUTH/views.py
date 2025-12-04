from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

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
                {"error": "Login failed", "details": str(e)},
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
        
        
# ---------------------------
# Update Score View
# ---------------------------
class UpdateScoreView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            profile = request.user.profile
            new_score = request.data.get("score")

            if new_score is None:
                return Response(
                    {"error": "Score is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # تأكد أن score رقم وليس نص
            try:
                new_score = int(new_score)
            except:
                return Response(
                    {"error": "Score must be a number"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            profile.score = new_score
            profile.save()

            return Response(
                {
                    "message": "Score updated successfully",
                    "score": profile.score
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Score update failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )