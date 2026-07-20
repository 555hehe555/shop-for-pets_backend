from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)

from api.serializers.cart import CartSerializer

cart_list = extend_schema(
    tags=["Carts"],
    summary="Get cart items",
    description="Returns a list of shopping cart items for the selected product.",
    responses={
        200: CartSerializer,
    },
)

cart_create = extend_schema(
    tags=["Carts"],
    summary="Add product to cart",
    description="Creates a new cart item for the authenticated user.",
    request=CartSerializer,
    responses={
        201: CartSerializer,
        400: OpenApiResponse(description="Validation error"),
    },
)

cart_retrieve = extend_schema(
    tags=["Carts"],
    summary="Retrieve cart item",
    description="Returns detailed information about a specific cart item.",
    responses={
        200: CartSerializer,
        404: OpenApiResponse(description="Cart item not found"),
    },
)

cart_delete = extend_schema(
    tags=["Carts"],
    summary="Delete cart item",
    description="Removes the selected item from the shopping cart.",
    responses={
        204: OpenApiResponse(description="Cart item deleted"),
        404: OpenApiResponse(description="Cart item not found"),
    },
)

cart_patch = extend_schema(
    tags=["Carts"],
    summary="Patch cart item",
    description="Patch the selected item from the shopping cart.",
    responses={
        200: OpenApiResponse(description="Cart item patched"),
        404: OpenApiResponse(description="Cart item not found"),
    },
)
