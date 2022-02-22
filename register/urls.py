from django.urls import path
from . import views
from .views import SignIn, SignUp, RegSignIn, UserView, Logout

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name = 'register'

urlpatterns = [
    path('sign_in/', SignIn.as_view(), name='sign_in'),
    path('sign_up/', SignUp.as_view(), name='sign_up'),
    path('logout/', views.logout_view, name='logout'),
    path('sign_in/profile', views.in_profile, name='profile'),
    path('sign_up/profile', views.in_profile, name='profile'),
    # path('api/sign_up/', views.sign_up_api, name='sign_up_api'),
    # path('api/sign_in/', RegSignIn.as_view(), name='sign_in_api'),
    path('api/user/', UserView.as_view(), name='sign_in_api'),
    path('api/logout', Logout.as_view(), name='logout_api'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
