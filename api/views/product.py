from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from documentation.product import (
    product_create_doc,
    product_delete_doc,
    product_list_doc,
    product_retrieve_doc,
    product_update_doc,
)
from documentation.product_image import (
    product_image_create_doc,
    product_image_delete_doc,
    product_image_partical_update_doc,
)
from ..models import Product, ProductImage
from ..permissions import *
from ..serializers.product import ProductImageSerializer, ProductSerializer


@extend_schema_view(
    list=product_list_doc,
    retrieve=product_retrieve_doc,
    create=product_create_doc,
    destroy=product_delete_doc,
    update=product_update_doc,
    partial_update=product_update_doc,
    add_image=product_image_create_doc,
    delete_image=product_image_delete_doc,
    update_image=product_image_partical_update_doc,
)
class ProductViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "delete", "put", "patch"]
    serializer_class = ProductSerializer
    queryset = Product.objects.prefetch_related("images").order_by(
        "-created_at",
        "-id",
    )

    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description"]


    def get_image(self, product, image_id):
        return get_object_or_404(
            ProductImage,
            pk=image_id,
            product=product,
        )

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            permission_classes = [permissions.AllowAny]

        elif self.action in (
            "create",
            "destroy",
            "update",
            "partial_update",
            "add_image",
            "delete_image",
            "update_image",
        ):
            permission_classes = [permissions.IsAdminUser]

        else:
            permission_classes = [IsSuperUser]

        return [permission() for permission in permission_classes]

    @extend_schema(
        request=ProductImageSerializer,
        responses={201: ProductImageSerializer},
    )
    @action(
        methods=["post"],
        detail=True,
        url_path="images",
    )
    def add_image(self, request, pk=None):
        product = self.get_object()

        serializer = ProductImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(product=product)

        return Response(serializer.data, status=201)

    @extend_schema(
        responses={204: None},
    )
    @action(
        methods=["delete"],
        detail=True,
        url_path=r"images/(?P<image_id>\d+)",
    )
    def delete_image(self, request, pk=None, image_id=None):
        product = self.get_object()
        image = self.get_image(product, image_id)

        image.delete()

        return Response(status=204)

    @extend_schema(
        request=ProductImageSerializer,
        responses={200: ProductImageSerializer},
    )
    @action(
        methods=["patch"],
        detail=True,
        url_path=r"images/(?P<image_id>\d+)",
    )
    def update_image(self, request, pk=None, image_id=None):
        product = self.get_object()
        image = self.get_image(product, image_id)

        serializer = ProductImageSerializer(
            image,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
