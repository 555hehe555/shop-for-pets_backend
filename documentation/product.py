from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status

from api.serializers.product import ProductSerializer


product_list_doc = extend_schema(
    tags=["Products"],
    description="get all products",
    request=None,
    responses={
        status.HTTP_200_OK: ProductSerializer(many=True),
    },
)

product_retrieve_doc = extend_schema(
    tags=["Products"],
    description="get info about one product",
    request=None,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=ProductSerializer,
            description="Product details.",
            examples=[
                OpenApiExample(
                    name="Success response",
                    value={
                        "id": 2,
                        "title": "sdsdedrfd",
                        "description": "strsssssssggsrgsedging",
                        "price": "9.00",
                        "is_available": True,
                        "created_at": "2026-07-13T14:26:08.678137Z",
                        "updated_at": "2026-07-13T14:26:08.678137Z",
                    },
                    response_only=True,
                )
            ],
        ),
    },
)

product_create_doc = extend_schema(
    tags=["Products"],
    description="create product",
    request=ProductSerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response=ProductSerializer,
            description="Product created successfully.",
            examples=[
                OpenApiExample(
                    name="Success created",
                    value={
                        "id": 0,
                        "title": "string",
                        "description": "string",
                        "price": "7037.69",
                        "is_available": True,
                        "created_at": "2026-07-13T14:53:47.484Z",
                        "updated_at": "2026-07-13T14:53:47.484Z",
                    },
                    response_only=True,
                )
            ],
        )
    },
)


product_update_doc = extend_schema(
    tags=["Products"],
    description="Update product",
    request=ProductSerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=ProductSerializer,
            description="Product updated successfully.",
            examples=[
                OpenApiExample(
                    name="Created response",
                    value={
                        "id": 0,
                        "title": "string",
                        "description": "string",
                        "price": "413017",
                        "is_available": True,
                        "created_at": "2026-07-13T14:58:38.037Z",
                        "updated_at": "2026-07-13T14:58:38.037Z",
                    },
                    response_only=True,
                )
            ],
        )
    },
)


product_delete_doc = extend_schema(
    tags=["Products"],
    description="Delete product",
    request=None,
    responses={status.HTTP_204_NO_CONTENT: ProductSerializer(many=True)},
)
