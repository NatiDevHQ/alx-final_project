
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .serializers import UserCreateSerializer, UserListSerializer

User = get_user_model()


# Register new users
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


# List all users (requires login)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
