from drf_spectacular.utils import extend_schema

from api.serializers.pet import PetSerializer

pet_list_doc = extend_schema(
    tags=["Pets"],
    summary="Get pets",
    description="Returns a list of pets belonging to the authenticated user.",
    responses={
        200: PetSerializer(many=True),
    },
)


pet_retrieve_doc = extend_schema(
    tags=["Pets"],
    summary="Get pet",
    description="Returns detailed information about a specific pet.",
    responses={
        200: PetSerializer,
    },
)


pet_create_doc = extend_schema(
    tags=["Pets"],
    summary="Create pet",
    description="Creates a new pet for the authenticated user.",
    request=PetSerializer,
    responses={
        201: PetSerializer,
    },
)


pet_update_doc = extend_schema(
    tags=["Pets"],
    summary="Update pet",
    description="Updates all editable fields of a pet.",
    request=PetSerializer,
    responses={
        200: PetSerializer,
    },
)


pet_patch_doc = extend_schema(
    tags=["Pets"],
    summary="Partially update pet",
    description="Updates selected fields of a pet.",
    request=PetSerializer,
    responses={
        200: PetSerializer,
    },
)


pet_delete_doc = extend_schema(
    tags=["Pets"],
    summary="Delete pet",
    description="Deletes a pet belonging to the authenticated user.",
    responses={
        204: None,
    },
)