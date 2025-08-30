from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserCreateView, UserListView

app_name = "users"

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),               # GET (admin only)
    path("register/", UserCreateView.as_view(), name="user-create"),  # POST
    path("login/", obtain_auth_token, name="login"),                  # POST -> token
]
