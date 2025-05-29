from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import coreapi
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from ..albuns.models import Album
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from .models import User
from rest_framework.serializers import ModelSerializer
from django.shortcuts import get_object_or_404

from ..sticker_groups.models import StickerGroup
from ..stickers.models import Sticker


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
        picture = request.data.get("picture")
        if not username or not password or not email:
            return Response({"error": "Preencha todos os campos"}, status=status.HTTP_400_BAD_REQUEST)


        with transaction.atomic():
            # Create user and album
            user = User.objects.create_user(username=username, password=password, email=email, picture=picture)
            album = Album.objects.create(user_id=user.id)

            # Create Sticker Groups
            self.create_stickers_for_album(album)

        return Response({"message": "Usuário criado com sucesso!"}, status=status.HTTP_201_CREATED)

    def create_stickers_for_album(self, album):
        # Retrieve all existing sticker groups and map them by their ID for proper referencing
        sticker_groups = {
            group.id: group for group in StickerGroup.objects.all()
        }

        # Define the sticker creation logic based on your algorithm
        sticker_definitions = [
            # Sticker group 0
            [
                {"text": "00", "idGroup": 0, "quantity": 0},
                {"text": "FWC 1", "idGroup": 0, "quantity": 0},
                {"text": "FWC 2", "idGroup": 0, "quantity": 1},
                {"text": "FWC 3", "idGroup": 0, "quantity": 0},
                {"text": "FWC 4", "idGroup": 0, "quantity": 3},
                {"text": "FWC 5", "idGroup": 0, "quantity": 2},
                {"text": "FWC 6", "idGroup": 0, "quantity": 0},
                {"text": "FWC 7", "idGroup": 0, "quantity": 2},
            ],
            # Sticker group 1
            [
                {"text": f"FWC {i}", "idGroup": 1, "quantity": i % 2}
                for i in range(8, 18)
            ],
            # Sticker group 2
            [
                {"text": "FWC 18", "idGroup": 2, "quantity": 0},
            ],
            # Sticker group 3 onwards
            *[
                [
                    {"text": f"{group_name} {i}", "idGroup": group_id, "quantity": i % 3}
                    for i in range(1, 21)
                ]
                for group_id, group_name in enumerate(
                    ["QAT", "ECU", "SEN", "NED", "ENG", "IRN", "USA", "WAL", "ARG", "KSA", "MEX", "POL",
                     "FRA", "AUS", "DEN", "TUN", "ESP", "CRC", "GER", "JPN", "BEL", "CAN", "MAR", "CRO",
                     "BRA", "SRB", "SUI", "CMR", "POR", "GHA", "URU", "KOR"],
                    start=4,
                )
            ],
        ]

        # Iterate over the defined stickers and create them
        for group in sticker_definitions:
            for sticker_data in group:
                # Retrieve the correct StickerGroup object using idGroup
                sticker_group = sticker_groups.get(sticker_data["idGroup"])
                if not sticker_group:
                    # Skip if the group does not exist (safety check)
                    continue

                # Create the Sticker object, directly passing the StickerGroup object (not the ID)
                Sticker.objects.create(
                    text=sticker_data["text"],
                    name=sticker_data["text"],  # Assuming name is the same as text
                    sticker_group=sticker_group,  # Pass the actual StickerGroup object
                    album=album,  # Pass the actual Album object
                    amount=sticker_data["quantity"],
                )



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

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
  # Include all fields of the User model


# View for fetching user information by id
class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]  # Authentication required
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = get_object_or_404(User, pk=user_id)  # Fetch the user by ID
        data = self.serializer_class(user).data  # Serialize the user instance
        return Response(data)
