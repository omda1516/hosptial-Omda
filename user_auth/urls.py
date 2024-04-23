from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenBlacklistView


app_name = 'auth'

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='user-login'),
    path('logout/', TokenBlacklistView.as_view(), name='user-logout'),
    path('signup/', views.RegisterView.as_view(), name='user-signup'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
