from math import ceil
from rest_framework.pagination import LimitOffsetPagination


class CustomOffSetPagination(LimitOffsetPagination):
    default_limit = 25
    max_limit = 100


def pagination(instances, serializer_class, request, **kwargs):
    page = request.query_params.get('page', 1)
    limit = request.query_params.get('limit', 25)

    try:
        page = int(page)
        limit = int(limit)
    except ValueError:
        page = 1
        limit = 25

    total_count = instances.count()
    offset = (page - 1) * limit
    paginated_instances = instances[offset:offset + limit]

    serializer = serializer_class(paginated_instances, many=True, **kwargs)

    response_data = {
        "current_page": page,
        "limit": limit,
        "pages": ceil(total_count / limit),
        "data_count": total_count,
        "data": serializer.data
    }

    return response_data


