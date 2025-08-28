from rest_framework import serializers
from .models import Task
      
class TaskSerializer(serializers.ModelSerializer):
    # Add read-only fields to show in responses but not required in requests
    user = serializers.ReadOnlyField(source='user.username')
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = ('user', 'id', 'title', 'description', 'completed', 'created_at', 'updated_at')
        
    def validate_title(self, value):
        """Validate that title is at least 3 characters long"""
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value