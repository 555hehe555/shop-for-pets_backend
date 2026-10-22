from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions, viewsets

from documentation.pet import (
    pet_create_doc,
    pet_delete_doc,
    pet_list_doc,
    pet_patch_doc,
    pet_retrieve_doc,
    pet_update_doc,
)
from ..models import Pet
from ..permissions import IsOwnerOrSuperUser
from ..serializers.pet import PetSerializer


@extend_schema_view(
    list=pet_list_doc,
    retrieve=pet_retrieve_doc,
    create=pet_create_doc,
    destroy=pet_delete_doc,
    update=pet_update_doc,
    partial_update=pet_patch_doc,
)
class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Pet.objects.all().order_by("-birthday", "-id")

        return Pet.objects.filter(owner=user).order_by("-birthday", "-id")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ["list", "create"]:
            permission_classes = [permissions.IsAuthenticated]

        elif self.action in ["retrieve", "update", "partial_update", "destroy"]:
            permission_classes = [IsOwnerOrSuperUser]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]