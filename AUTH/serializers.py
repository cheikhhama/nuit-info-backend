from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken,TokenError



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})

        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})

        
        
        if len(attrs['password']) < 6:
            raise serializers.ValidationError({"password": "Password must be at least 6 characters."})

        return attrs

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user
        except Exception as e:
            raise serializers.ValidationError({"error": "Failed to create user."})
    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError({"detail": "Username and password are required."})

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError({"detail": "Invalid username or password"})

        try:
            refresh = RefreshToken.for_user(user)
        except Exception:
            raise serializers.ValidationError({"detail": "Token generation failed."})

        # جلب score من Profile
        profile = user.profile  # لأن signals أنشأت profile تلقائياً

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "username": user.username,
            "email": user.email,
            "score": profile.score,  # ← هذا أهم شيء
        }



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs.get("refresh")

        if not self.token:
            raise serializers.ValidationError({"refresh": "Refresh token is required"})

        return attrs

    def save(self, **kwargs):
        try:
            # Blacklist refresh token (invalidate)
            RefreshToken(self.token).blacklist()

        except TokenError:
            raise serializers.ValidationError({"refresh": "Invalid or expired refresh token"})
        
from rest_framework import serializers
from .models import Quiz, Reponse


class ReponseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    label = serializers.CharField(source='texte')
    isCorrect = serializers.BooleanField(source='est_correct')

    class Meta:
        model = Reponse
        fields = ('id', 'label', 'isCorrect')

class QuizSerializer(serializers.ModelSerializer):
    options = ReponseSerializer(source='reponses', many=True)
    categorie = serializers.CharField(source='categorie.nom')

    class Meta:
        model = Quiz
        fields = ('id', 'titre', 'contenu', 'categorie', 'options')


from rest_framework import serializers
from .models import Categorie

class CategorieWithQuizCountSerializer(serializers.ModelSerializer):
    quiz_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Categorie
        fields = ['id', 'nom', 'quiz_count']


class ReponseCheckSerializer(serializers.Serializer):
    reponse_id = serializers.IntegerField()
