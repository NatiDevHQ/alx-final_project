from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'tasks'


router = routers.DefaultRouter()
router.register('', views.TaskViewSet, basename='tasks')


urlpatterns = [
    path('', include(router.urls)),
]