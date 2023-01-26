from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import registration_view, logout_view, user_list_view
from . import views

urlpatterns = [
    path('login/',views.CustomAuthToken.as_view(),name = 'login'),
    path('register/',registration_view,name = 'register'),
    path('logout/',logout_view,name = 'logout'),
    path('user/list/',user_list_view,name="user_list"),
]