from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from django.core.mail import EmailMessage
from .models import CustomUser
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, NotAuthenticated, ValidationError
import jwt, datetime
from decouple import config
from django.contrib.auth.password_validation import (
  CommonPasswordValidator,
  MinimumLengthValidator,
  NumericPasswordValidator,
  UserAttributeSimilarityValidator,
)
import re
from django.conf import settings
from rest_framework import status

class CustomUserView(APIView):
  def get(self, request, format = 'json'):
    jwt_token = request.COOKIES.get('jwt', None)
    auth_token = request.headers.get('Authorization', None)
    
    if auth_token is None:
      raise PermissionDenied('No authorization token was provided')
    
    if auth_token != config('AUTHORIZATION_TOKEN'):
      raise PermissionDenied('Wrong authorization token')
    
    if jwt_token is None:
      raise NotAuthenticated('Unauthenticated')
    
    try:
      payload = jwt.decode(jwt_token, 'secret', algorithms = ["HS256"])
    except jwt.ExpiredSignatureError:
      raise NotAuthenticated("Authentication token has expired")
    
    user = CustomUser.objects.filter(id = payload['id']).first()
    
    serializer = CustomUserSerializer(user)
    
    return Response(serializer.data)
  
  def post (self, request, format = 'json'):
    auth_token = request.headers.get('Authorization', None)
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    phone = request.POST.get('phone', None)
    age = request.POST.get('age', None)
    
    if auth_token is None:
      raise PermissionDenied('No authorization token was provided')
    
    if auth_token != config('AUTHORIZATION_TOKEN'):
      raise PermissionDenied('Wrong authorization token')
    
    if CustomUser.objects.filter(email = email).exists():
      raise ValidationError('User already exists')
    
    if email is None:
      raise ValidationError('Email is required')
    
    if password is None:
      raise ValidationError('Password is required')
    
    if age is None:
      raise ValidationError('Age is required')
    
    password_validators = [
      MinimumLengthValidator(),
      CommonPasswordValidator(),
      NumericPasswordValidator(),
      UserAttributeSimilarityValidator()
    ]
    password_validation_errors = []
    for validator in password_validators:
      try :
        validator.validate(password)
      except Exception as e:
        password_validation_errors.extend(e.messages)
    
    if password_validation_errors:
      raise ValidationError('\n'.join(password_validation_errors))
    
    pattern1 = r'^\+\d{2} \(\d{2}\) \d{5}-\d{4}$'  # +99 (99) 99999-9999
    pattern2 = r'^\+\d{3} \(\d{2}\) \d{5}-\d{4}$'  # +999 (99) 99999-9999
    
    if not (re.match(pattern1, phone) or re.match(pattern2, phone)):
      raise ValidationError("Invalid phone number")
    
    if age > 99:
      raise ValidationError('Invalid age')
    
    serializer = CustomUserSerializer(data = request.data)
    if (serializer.is_valid()):
      user = serializer.save()
      if user:
        email_message = EmailMessage(
          'Please confirm your account',
          'Follow below your confirmation code: \n{user.token_code}',
          settings.EMAIL_HOST_USER,
          [request.data['email']]
        )
        email_message.fail_silently = False
        email_message.send()
        json = serializer.data
        
        return Response(json, status = status.HTTP_201_CREATED)
      return Response(json, status = status.HTTP_403_FORBIDDEN)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):
  def post(self, request): 
    auth_token = request.headers.get('Authorization', None)
    email = request.POST.get('email', None)
    password = request.get('password', None)
    user = CustomUser.objects.filter(email = email).first()
    
    if auth_token is None:
      raise PermissionDenied('No authorization token was provided')
    
    if auth_token != config('AUTHORIZATION_TOKEN'):
      raise PermissionDenied('Wrong authorization token')
    
    if email is None:
      raise ValidationError('Email is required')
    
    if password is None:
      raise ValidationError('Password is required')
    
    if user is None:
      raise AuthenticationFailed('User not found')
    
    if not user.check_password(password):
      raise AuthenticationFailed("Incorrect password")
    
    payload = {
      'id': user.id,
      'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
      'iat': datetime.datetime.utcnow()
    }
    
    token = jwt.encode(payload, 'secret', algorithm= 'HS256')
    
    response = Response()
    
    response.set_cookie(key = 'jwt', value = token, httponly = True)
    
    response.data = {
      'Message':'Token successfully created'
    }
    
    return response
  
# class SendConfirmationTokenView(APIView):
#   def post(self, request, format = 'json'):
#     jwt_token = request.COOKIES.get('jwt')
#     auth_token = request.headers.get('Authorization')