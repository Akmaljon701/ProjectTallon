from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from user.serializers import CustomUserSerializer, CustomUserGetSerializer
from utils.responses import response_schema

create_user_schema = extend_schema(
    summary="Admin create user",
    request=CustomUserSerializer,
    responses=response_schema
)

update_user_schema = extend_schema(
    summary="Admin update user",
    request=CustomUserSerializer,
    responses=response_schema,
    parameters=[
        OpenApiParameter(name='pk', description='User ID', required=True, type=OpenApiTypes.INT),
    ]
)

get_users_schema = extend_schema(
    summary="Admin get users",
    request=None,
    responses=CustomUserGetSerializer(many=True),
)

get_current_user_schema = extend_schema(
    summary="Get current user",
    responses=CustomUserGetSerializer
)

