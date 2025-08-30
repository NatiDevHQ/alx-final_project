from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'user', 'completed', 'created_at')
	list_filter = ('completed', 'created_at', 'user')
	list_editable = ('completed',)
	search_fields = ('title', 'description', 'user__username')
	ordering = ('-created_at',)
