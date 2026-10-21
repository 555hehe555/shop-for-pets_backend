from rest_framework import permissions, viewsets

from ..models import Pet
from ..permissions import IsOwnerOrSuperUser
from ..serializers.pet import PetSerializer


# @extend_schema_view(
#     list=product_list_doc,
#     retrieve=product_retrieve_doc,
#     create=product_create_doc,
#     destroy=product_delete_doc,
#     update=product_update_doc,
#     partial_update=product_update_doc,
# )
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