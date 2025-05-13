from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import coreapi
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User



class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        if not username or not password or not email:
            return Response({"error": "Preencha todos os campos"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({"message": "Usuário criado com sucesso!"}, status=status.HTTP_201_CREATED)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            })
        return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
