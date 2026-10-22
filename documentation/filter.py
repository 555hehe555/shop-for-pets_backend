from drf_spectacular.utils import extend_schema

from api.serializers.filter import (
    SpeciesSerializer,
    CategorySerializer,
    BrandSerializer,
)

species_list_doc = extend_schema(
    tags=["Filters"],
    summary="Get species",
    description="Returns a list of available animal species for filters.",
    responses={
        200: SpeciesSerializer(many=True),
    },
)


category_list_doc = extend_schema(
    tags=["Filters"],
    summary="Get categories",
    description="Returns a list of available product categories for filters.",
    responses={
        200: CategorySerializer(many=True),
    },
)


brand_list_doc = extend_schema(
    tags=["Filters"],
    summary="Get brands",
    description="Returns a list of available brands for filters.",
    responses={
        200: BrandSerializer(many=True),
    },
)