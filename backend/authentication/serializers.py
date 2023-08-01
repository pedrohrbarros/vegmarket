from rest_framework import serializers

from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ('id', 'name', 'email', 'password', 'phone', 'age', 'token_code', 'start_date', 'is_staff')
    
    extra_kwargs = {
      'password': {'write_only': True},
      'token_code': {'write_only': True}
    }
    
    def create(self, validated_data):
      email = validated_data.pop('email', None)
      password = validated_data.pop('password', None)
      instance = self.Meta.model(**validated_data)
      if (password is not None):
        instance.set_password(password)
      if CustomUser.objects.filter(email = email).exists():
        raise serializers.ValidationError('User already exists')
      instance.save()
      return instance