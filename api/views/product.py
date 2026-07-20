from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema_view

from documentation.product import (
    product_list_doc,
    product_create_doc,
    product_retrieve_doc,
    product_update_doc,
    product_delete_doc,
)
from ..models import Product

from ..serializers.product import ProductSerializer


@extend_schema_view(
    list=product_list_doc,
    retrieve=product_retrieve_doc,
    create=product_create_doc,
    destroy=product_delete_doc,
    update=product_update_doc,
    partial_update=product_update_doc,
)
class ProductViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "delete", "put", "patch"]
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("-created_at", "-id")

    def get_permissions(self):
        if self.action in ["list", "retrieve", "create", "post_list"]:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        if self.action == "create":
            return ProductSerializer
        if self.action in ["update", "partial_update"]:
            return ProductSerializer
        return ProductSerializer
