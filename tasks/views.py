import csv
import xlwt
from xlwt import Workbook 
from django.http import HttpResponse
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwner

class TaskViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """
        List my all completed tasks.
        """
        tasks = Task.objects.filter(
            user=request.user,
            completed=True
        )
        page = self.paginate_queryset(tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def incompleted(self, request):
        """
        List all incompleted tasks.
        """
        tasks = Task.objects.filter(
            user=request.user, 
            completed=False
        )
        page = self.paginate_queryset(tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        """
        Export data to csv file.
        """
       
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tasks_rate.csv"'

        user_name = request.user.username

      
        completed_tasks = Task.objects.filter(
            user=request.user, completed=True).count()

      
        incompleted_tasks = Task.objects.filter(
            user=request.user, completed=False).count()

        
        all_tasks = Task.objects.filter(user=request.user).count()

        
        rate = 100
        if all_tasks > 0:
            rate = round((completed_tasks * 100) / all_tasks, 1)

        writer = csv.writer(response)

       
        writer.writerow(['Username', f'{user_name}'])
        writer.writerow([])
        writer.writerow(['All Tasks', 'Completed', 'Incompleted', 'Rate'])
        writer.writerow([f'{all_tasks}', f'{completed_tasks}', f'{incompleted_tasks}', f'%{rate}'])

        return response
    
    @action(detail=False, methods=['get'])
    def export_xls(self, request):
        """
        Export data to excel file.
        """
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="tasks_rate.xls"'

        
        wb = Workbook() 

        
        sheet1 = wb.add_sheet('Ratio') 

        name_style = xlwt.easyxf('font: bold 1, color red')
        style = xlwt.easyxf('font: bold 1')

        user_name = request.user.username

        sheet1.write(0, 0, 'Username', name_style) 
        sheet1.write(0, 1, f'{user_name}', name_style)

        # Heads
        sheet1.write(2, 0, 'All Tasks', style)
        sheet1.write(2, 1, 'Completed', style)
        sheet1.write(2, 2, 'Incompleted', style)
        sheet1.write(2, 3, 'Rate', style)

        completed_tasks = Task.objects.filter(
            user=request.user, completed=True).count()

        incompleted_tasks = Task.objects.filter(
            user=request.user, completed=False).count()

        all_tasks = Task.objects.filter(user=request.user).count()

        rate = 100
        if all_tasks > 0:
            rate = round((completed_tasks * 100) / all_tasks, 1)

        sheet1.write(3, 0, f'{all_tasks}')
        sheet1.write(3, 1, f'{completed_tasks}')
        sheet1.write(3, 2, f'{incompleted_tasks}')
        sheet1.write(3, 3, f'%{rate}')

        # save the file.
        wb.save(response)

        return response