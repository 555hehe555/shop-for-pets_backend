from drf_spectacular.utils import extend_schema

from api.serializers.product import ProductImageSerializer

product_image_create_doc = extend_schema(
    tags=["Product image"],
    description="add image to product",
    summary="add image to product",
    responses={
        200: ProductImageSerializer(),
    },
)

product_image_delete_doc = extend_schema(
    tags=["Product image"],
    description="delete image to product",
    summary="delete image to product",
    responses={
        204: ProductImageSerializer(),
    },
)

product_image_partical_update_doc = extend_schema(
    tags=["Product image"],
    description="patch image to product",
    summary="patch image to product",
    responses={
        200: ProductImageSerializer(),
    },
)
