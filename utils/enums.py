from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from api.models import Tallon


@extend_schema(responses={
    200: {"description": "The operation was completed successfully", "example": dict(Tallon.TALLON_NUMBER_CHOICES)},
})
@api_view(['GET'])
@permission_classes([AllowAny])
def tallon_number_choices(request):
    choices = dict(Talon.TALLON_NUMBER_CHOICES)
    return JsonResponse(choices)
