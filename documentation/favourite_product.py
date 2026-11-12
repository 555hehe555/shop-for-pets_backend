from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)

from api.serializers.favourite_product import FavouriteProductSerializer

favourite_list = extend_schema(
    tags=["Favourites"],
    summary="Get favourite products",
    description="Returns a list of favourite products for the authenticated user.",
    responses={
        200: FavouriteProductSerializer,
    },
)

favourite_create = extend_schema(
    tags=["Favourites"],
    summary="Add product to favourites",
    description="Adds a product to the authenticated user's favourites. If the product is already in favourites, returns the existing record with 200.",
    request=FavouriteProductSerializer,
    responses={
        201: FavouriteProductSerializer,
        200: FavouriteProductSerializer,
        400: OpenApiResponse(description="Validation error"),
    },
)

favourite_retrieve = extend_schema(
    tags=["Favourites"],
    summary="Retrieve favourite product",
    description="Returns detailed information about a specific favourite product entry.",
    responses={
        200: FavouriteProductSerializer,
        404: OpenApiResponse(description="Favourite product not found"),
    },
)

favourite_delete = extend_schema(
    tags=["Favourites"],
    summary="Delete favourite product",
    description="Removes the selected product from the authenticated user's favourites.",
    responses={
        204: OpenApiResponse(description="Favourite product deleted"),
        404: OpenApiResponse(description="Favourite product not found"),
    },
)

