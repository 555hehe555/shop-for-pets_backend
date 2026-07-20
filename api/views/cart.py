from django.db import transaction
from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from documentation.cart import (
    cart_create,
    cart_delete,
    cart_list,
    cart_patch,
    cart_retrieve,
)

from ..models import Cart
from ..serializers.cart import CartPatchSerializer, CartSerializer


@extend_schema_view(
    list=cart_list,
    retrieve=cart_retrieve,
    create=cart_create,
    destroy=cart_delete,
    partial_update=cart_patch,
)
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    http_method_names = ["get", "post", "patch", "delete"]

    lookup_field = "product_id"
    lookup_url_kwarg = "product_id"

    def get_queryset(self):
        return (
            Cart.objects.filter(user=self.request.user)
            .select_related("product")
            .order_by("-created_at")
        )

    # noqa: F821
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data["product"]
        quantity = serializer.validated_data.get("quantity", 1)

        cart, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"quantity": quantity},
        )

        if not created:
            cart.quantity += quantity
            cart.save(update_fields=["quantity"])

        serializer = self.get_serializer(cart)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    def get_serializer_class(self):
        if self.action == "partial_update":
            return CartPatchSerializer
        return CartSerializer
