from rest_framework import serializers

from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
  
  password = serializers.CharField(min_length = 8, write_only = True)
  
  class Meta:
    model = CustomUser
    fields = ('id', 'name', 'email', 'password', 'phone', 'age', 'start_date', 'is_staff', 'is_active')
    
    extra_kwargs = {
      'password': {'write_only': True}
    }
    
  #Hash Password
  def create(self, validated_data):
    password = validated_data.pop('password', None)
    instance = self.Meta.model(**validated_data)
    
    instance.set_password(password)
    
    instance.save()
    return instance