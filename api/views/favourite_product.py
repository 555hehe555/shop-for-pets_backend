from django.db import transaction
from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from documentation.favourite_product import (
    favourite_create,
    favourite_delete,
    favourite_list,
    favourite_retrieve,
)

from ..models import FavouriteProduct
from ..serializers.favourite_product import FavouriteProductSerializer


@extend_schema_view(
    list=favourite_list,
    retrieve=favourite_retrieve,
    create=favourite_create,
    destroy=favourite_delete,
)
class FavouriteProductViewSet(viewsets.ModelViewSet):
    serializer_class = FavouriteProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    http_method_names = ["get", "post", "delete"]

    lookup_field = "product_id"
    lookup_url_kwarg = "product_id"

    def get_queryset(self):
        return (
            FavouriteProduct.objects.filter(user=self.request.user)
            .select_related("product")
            .order_by("-created_at")
        )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data["product"]

        favourite, created = FavouriteProduct.objects.get_or_create(
            user=request.user,
            product=product,
        )

        serializer = self.get_serializer(favourite)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
