from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status

from api.serializers.user import (
    GetCustomUserSerializer,
    CreateCustomUserSerializer,
    UpdateCustomUserSerializer,
    GetMeSerializer,
)

user_list_doc = extend_schema(
    tags=["Users"],
    description="Get paginated list of users.",
    request=None,
    responses={
        status.HTTP_200_OK: GetCustomUserSerializer(many=True),
    },
)

user_retrieve_doc = extend_schema(
    tags=["Users"],
    description="Get user details by id.",
    request=None,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=GetCustomUserSerializer,
            description="User details.",
            examples=[
                OpenApiExample(
                    name="Success response",
                    value={
                        "id": 1,
                        "username": "john_doe",
                        "first_name": "John",
                        "last_name": "Doe",
                        "full_name": "John Doe",
                        "email": "john.doe@example.com",
                        "phone_number": "+380501234567",
                        "date_of_birth": "1995-05-15",
                        "date_joined": "2026-04-14T12:00:00Z",
                        "last_login": "2026-04-14T13:00:00Z",
                        "is_active": True,
                        "is_staff": False,
                        "is_superuser": False,
                    },
                    response_only=True,
                )
            ],
        ),
    },
)

user_create_doc = extend_schema(
    tags=["Users"],
    description="Create a new user.",
    request=CreateCustomUserSerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response=CreateCustomUserSerializer,
            description="User created successfully.",
            examples=[
                OpenApiExample(
                    name="Created response",
                    value={
                        "id": 1,
                        "username": "john_doe",
                        "email": "john.doe@example.com",
                    },
                    response_only=True,
                )
            ],
        ),
    },
)

user_update_doc = extend_schema(
    tags=["Users"],
    description="Fully update user profile.",
    request=UpdateCustomUserSerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=GetCustomUserSerializer,
            description="User updated successfully.",
            examples=[
                OpenApiExample(
                    name="Updated response",
                    value={
                        "id": 1,
                        "username": "john_doe",
                        "first_name": "John",
                        "last_name": "Doe",
                        "full_name": "John Doe",
                        "email": "john.doe@example.com",
                        "phone_number": "+380501234567",
                        "date_of_birth": "1995-05-15",
                        "date_joined": "2026-04-14T12:00:00Z",
                        "last_login": "2026-04-14T13:00:00Z",
                        "is_active": True,
                        "is_staff": False,
                        "is_superuser": False,
                    },
                    response_only=True,
                )
            ],
        ),
    },
)

user_patch_doc = extend_schema(
    tags=["Users"],
    description="Partially update user profile.",
    request=UpdateCustomUserSerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=GetCustomUserSerializer,
            description="User partially updated successfully.",
            examples=[
                OpenApiExample(
                    name="Patched response",
                    value={
                        "id": 1,
                        "username": "john_doe",
                        "first_name": "John",
                        "last_name": "Doe",
                        "full_name": "John Doe",
                        "email": "john.doe@example.com",
                        "phone_number": "+380501234567",
                        "date_of_birth": "1995-05-15",
                        "date_joined": "2026-04-14T12:00:00Z",
                        "last_login": "2026-04-14T13:00:00Z",
                        "is_active": True,
                        "is_staff": False,
                        "is_superuser": False,
                    },
                    response_only=True,
                )
            ],
        ),
    },
)

user_delete_doc = extend_schema(
    tags=["Users"],
    description="Delete user.",
    request=None,
    responses={
        status.HTTP_204_NO_CONTENT: OpenApiResponse(
            response=None,
            description="User deleted successfully.",
        ),
    },
)

get_me_doc = extend_schema(
    tags=["Users"],
    description="Get current authenticated user.",
    request=None,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=GetMeSerializer,
            description="Current user details.",
            examples=[
                OpenApiExample(
                    name="Current user response",
                    value={
                        "id": 1,
                        "full_name": "John Doe",
                        "email": "john.doe@example.com",
                        "phone_number": "+380501234567",
                        "date_of_birth": "1995-05-15",
                    },
                    response_only=True,
                )
            ],
        ),
    },
)
