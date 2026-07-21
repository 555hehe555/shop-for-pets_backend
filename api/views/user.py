from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from documentation.login_user import login_user_list_doc
from documentation.user import (
    get_me_doc,
    user_create_doc,
    user_delete_doc,
    user_list_doc,
    user_patch_doc,
    user_retrieve_doc,
    user_update_doc,
)

from ..models import CustomUser
from ..permissions import IsOwnerOrAdminDelete
from ..serializers.user import (
    CreateCustomUserSerializer,
    GetCustomUserSerializer,
    GetMeSerializer,
    LoginCustomUserSerializer,
    UpdateCustomUserSerializer,
)


@extend_schema_view(
    list=user_list_doc,
    retrieve=user_retrieve_doc,
    create=user_create_doc,
    destroy=user_delete_doc,
    update=user_update_doc,
    partial_update=user_patch_doc,
)
class CustomUserViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "delete", "put", "patch"]
    serializer_class = GetCustomUserSerializer
    queryset = CustomUser.objects.all().order_by("-date_joined", "-id")

    def get_permissions(self):
        if self.action in ["list", "retrieve", "create", "post_list"]:
            return [permissions.AllowAny()]
        return [IsOwnerOrAdminDelete()]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateCustomUserSerializer
        if self.action in ["update", "partial_update"]:
            return UpdateCustomUserSerializer
        return GetCustomUserSerializer


@extend_schema_view(get=get_me_doc)
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses=GetMeSerializer,
    )
    def get(self, request):
        serializer = GetMeSerializer(request.user)
        return Response(serializer.data)


@extend_schema_view(login=login_user_list_doc)
class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = LoginCustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if user is None:
            raise AuthenticationFailed("Invalid credentials.")

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )
