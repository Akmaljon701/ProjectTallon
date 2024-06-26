from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from user.models import CustomUser
from user.schemas import create_user_schema, update_user_schema, get_users_schema, get_current_user_schema, \
    login_user_schema
from user.serializers import CustomUserSerializer, CustomUserGetSerializer, CustomTokenObtainPairSerializer
from utils.permissions import allowed_only_admin
from utils.responses import success
from rest_framework_simplejwt.tokens import RefreshToken


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': str(e)}, 400)

        return Response(serializer.validated_data, 200)


@create_user_schema
@api_view(['POST'])
@allowed_only_admin()
def create_user(request):
    serializer = CustomUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


@update_user_schema
@api_view(['PUT'])
@allowed_only_admin()
def update_user(request):
    pk = request.query_params.get('pk')
    user = CustomUser.objects.get(id=pk)
    serializer = CustomUserSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


@get_users_schema
@api_view(['GET'])
@allowed_only_admin()
def get_users(request):
    users = CustomUser.objects.select_related('branch').all().order_by('full_name')
    serializor = CustomUserGetSerializer(users, many=True)
    return Response(serializor.data, 200)


@get_current_user_schema
@api_view(['GET'])
def get_current_user(request):
    serializer = CustomUserGetSerializer(request.user)
    return Response(serializer.data, 200)

