from django.urls import path, include
from rest_framework import routers
from tasks import views

app_name = 'tasks'

router = routers.DefaultRouter()
# Keep base at /tasks/
router.register('', views.TaskView, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),

    # Optional helper endpoints (redundant with filtered list, but OK)
    path('me/all/', views.my_tasks, name='my-tasks'),
    path('me/<int:pk>/', views.task_detail, name='task-detail'),

    path('me/completed/', views.tasks_completed, name='completed'),
    path('me/incompleted/', views.tasks_incompleted, name='incomplete'),

    # Export (now protected)
    path('export/csv/', views.save_as_csv, name='save-as-csv'),
    path('export/xls/', views.save_as_xls, name='save-as-xls'),
]
