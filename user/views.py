from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from user.models import CustomUser
from user.schemas import create_user_schema, update_user_schema, get_users_schema, get_current_user_schema, \
    login_user_schema
from user.serializers import CustomUserSerializer, CustomUserGetSerializer, CustomTokenObtainPairSerializer
from utils.permissions import allowed_only_admin
from utils.responses import success
from rest_framework_simplejwt.tokens import RefreshToken


@login_user_schema
@api_view(['POST'])
@permission_classes([AllowAny])
def custom_token_obtain_pair(request):
    serializer = CustomTokenObtainPairSerializer(data=request.data)

    try:
        serializer.is_valid(raise_exception=True)

        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            ser = CustomUserGetSerializer(user)
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                # 'user': ser.data
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=401)
    except Exception as e:
        return Response({'detail': str(e)}, status=400)


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

