from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from api.serializers import BranchSerializer
from utils.responses import response_schema

create_branch_schema = extend_schema(
    summary="Admin create branch",
    request=BranchSerializer,
    responses=response_schema
)

update_branch_schema = extend_schema(
    summary="Admin update branch",
    request=BranchSerializer,
    responses=response_schema,
    parameters=[
        OpenApiParameter(name='pk', description='Branch ID', required=True, type=OpenApiTypes.INT),
    ]
)

get_branches_schema = extend_schema(
    summary="Admin get branches",
    request=None,
    responses=BranchSerializer(many=True),
)

create_organization_schema = extend_schema(
    summary="Admin create organization",
    request=BranchSerializer,
    responses=response_schema
)

update_organization_schema = extend_schema(
    summary="Admin update organization",
    request=BranchSerializer,
    responses=response_schema,
    parameters=[
        OpenApiParameter(name='pk', description='Organization ID', required=True, type=OpenApiTypes.INT),
    ]
)

get_organizations_schema = extend_schema(
    summary="Admin get organizations",
    request=None,
    responses=BranchSerializer(many=True),
    parameters=[
        OpenApiParameter(name='pk', description='Branch ID', required=True, type=OpenApiTypes.INT),
    ]
)

get_tallon_table_data_all_schema = extend_schema(
    summary="Get tallon table 1 and 2",
    responses=None,
    parameters=[
        OpenApiParameter(name='from_date', description='YYY-MM-DD', required=False, type=OpenApiTypes.DATE),
        OpenApiParameter(name='to_date', description='YYY-MM-DD', required=False, type=OpenApiTypes.DATE),
    ]
)

get_tallon_table_data_detail_schema = extend_schema(
    summary="Get tallon table 3",
    responses=None,
    parameters=[
        OpenApiParameter(name='branch_pk', description='Branch ID', required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='organization_pk', description='Organization ID', required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='from_date', description='YYY-MM-DD', required=False, type=OpenApiTypes.DATE),
        OpenApiParameter(name='to_date', description='YYY-MM-DD', required=False, type=OpenApiTypes.DATE),
    ]
)
