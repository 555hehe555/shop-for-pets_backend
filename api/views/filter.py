from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions, viewsets
from rest_framework.mixins import ListModelMixin

from documentation.filter import (
    species_list_doc,
    category_list_doc,
    brand_list_doc,
)
from ..models import Species, Category, Brand
from ..serializers.filter import (
    SpeciesSerializer,
    CategorySerializer,
    BrandSerializer,
)


@extend_schema_view(
    list=species_list_doc,
)
class SpeciesViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = Species.objects.all().order_by("name")
    serializer_class = SpeciesSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    list=category_list_doc,
)
class CategoryViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    list=brand_list_doc,
)
class BrandViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = Brand.objects.all().order_by("name")
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]