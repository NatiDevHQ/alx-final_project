from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    # Prevent client from setting someone else as owner.
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = ('id', 'user', 'title', 'description', 'completed', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
