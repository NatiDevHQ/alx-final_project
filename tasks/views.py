import csv
import xlwt
from xlwt import Workbook
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsOwner
from .serializers import TaskSerializer
from .models import Task

class TaskView(viewsets.ModelViewSet):
    """
    Provides list, create, retrieve, update, destroy for authenticated user's tasks.
    """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = TaskSerializer

    def get_queryset(self):
        # Critical: restrict to the requesting user
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # Enforce ownership on create
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):
    try:
        task = Task.objects.get(user=request.user, pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TaskSerializer(task)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, completed=True)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tasks_incompleted(request):
    tasks = Task.objects.filter(user=request.user, completed=False)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def save_as_csv(request):
    """
    Export current user's task stats as CSV.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks_rate.csv"'

    user_name = request.user.username
    completed_tasks = Task.objects.filter(user=request.user, completed=True).count()
    incompleted_tasks = Task.objects.filter(user=request.user, completed=False).count()
    all_tasks = completed_tasks + incompleted_tasks

    rate = 0
    if all_tasks > 0:
        rate = round((completed_tasks * 100) / all_tasks, 1)

    writer = csv.writer(response)
    writer.writerow(['Username', f'{user_name}'])
    writer.writerow([])
    writer.writerow(['All Tasks', 'Completed', 'Incomplete', 'Completion %'])
    writer.writerow([f'{all_tasks}', f'{completed_tasks}', f'{incompleted_tasks}', f'{rate}%'])
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def save_as_xls(request):
    """
    Export current user's task stats as XLS.
    """
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="tasks_rate.xls"'

    wb = Workbook()
    sheet1 = wb.add_sheet('Ratio')

    name_style = xlwt.easyxf('font: bold 1')
    header_style = xlwt.easyxf('font: bold 1')

    user_name = request.user.username
    sheet1.write(0, 0, 'Username', name_style)
    sheet1.write(0, 1, f'{user_name}', name_style)

    # Headings
    sheet1.write(2, 0, 'All Tasks', header_style)
    sheet1.write(2, 1, 'Completed', header_style)
    sheet1.write(2, 2, 'Incomplete', header_style)
    sheet1.write(2, 3, 'Completion %', header_style)

    completed_tasks = Task.objects.filter(user=request.user, completed=True).count()
    incompleted_tasks = Task.objects.filter(user=request.user, completed=False).count()
    all_tasks = completed_tasks + incompleted_tasks

    rate = 0
    if all_tasks > 0:
        rate = round((completed_tasks * 100) / all_tasks, 1)

    sheet1.write(3, 0, f'{all_tasks}')
    sheet1.write(3, 1, f'{completed_tasks}')
    sheet1.write(3, 2, f'{incompleted_tasks}')
    sheet1.write(3, 3, f'{rate}%')

    wb.save(response)
    return response
