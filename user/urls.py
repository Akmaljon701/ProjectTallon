from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user.views import create_user, update_user, get_users, get_current_user, custom_token_obtain_pair

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create/', create_user, name='create_user'),
    path('update/', update_user, name='update_user'),
    path('all/', get_users, name='get_users'),
    path('current/', get_current_user, name='get_current_user'),
]
