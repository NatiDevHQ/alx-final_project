from django.urls import include, path
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserCreateView, UserListView

app_name = "users"

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),                           # GET all users (auth required)
    path("register/", UserCreateView.as_view(), name="user-create"),              # POST register new user
    path("login/", obtain_auth_token, name="login"),                              # POST username+password -> token
]
