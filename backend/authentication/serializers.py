from rest_framework import serializers

from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = CustomUser
    fields = ('id', 'name', 'email', 'password', 'phone', 'age', 'start_date', 'is_staff')
    
    extra_kwargs = {
      'password': {'write_only': True}
    }