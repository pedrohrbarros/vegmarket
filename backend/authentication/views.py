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
from django.template.loader import render_to_string

class CustomUserView(APIView):
  def get(self, request, format = 'json'):
    jwt_token = request.COOKIES.get('jwt', None)
    
    if jwt_token is None:
      raise NotAuthenticated('Unauthenticated')
    
    try:
      payload = jwt.decode(jwt_token, 'secret', algorithms = ["HS256"])
    except jwt.ExpiredSignatureError:
      raise NotAuthenticated('Wrong JWT authentication code')
    
    user = CustomUser.objects.filter(id = payload['id']).first()
    
    serializer = CustomUserSerializer(user)
    
    return Response(serializer.data)
  
  def post (self, request, format = 'json'):
    auth_token = request.headers.get('Authorization', None)
    
    if auth_token is None:
      raise PermissionDenied('No authorization token was provided')
    
    if auth_token != config('AUTHORIZATION_TOKEN'):
      raise PermissionDenied('Wrong authorization token')
    
    if 'name' not in request.data:
      raise ValidationError({'detail':'Name is required'})
    
    if 'email' not in request.data:
      raise ValidationError({'detail':'Email is required'})
    
    email = request.data['email']
    
    if 'password' not in request.data:
      raise ValidationError({'detail':'Password is required'})
    
    password = request.data['password']
    
    if 'age' not in request.data:
      raise ValidationError({'detail':'Age is required'})
    
    age = request.data['age']
    
    if age > 149:
      raise ValidationError({'detail':'Invalid age'})
    
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
      raise ValidationError({'detail':' '.join(password_validation_errors)})
    
    if 'phone' in request.data:
      phone = request.data['phone']
    
      pattern1 = r'^\+\d{2} \(\d{2}\) \d{5}-\d{4}$'  # +99 (99) 99999-9999
      pattern2 = r'^\+\d{3} \(\d{2}\) \d{5}-\d{4}$'  # +999 (99) 99999-9999
      
      if not (re.match(pattern1, phone) or re.match(pattern2, phone)):
        raise ValidationError({'detail':'Invalid phone number'})
    
    if CustomUser.objects.filter(email = email).exists():
      raise ValidationError({'detail':'User already exists'})
    
    request.data['is_staff'] = False

    # User will be active after the validation of the token code
    request.data['is_active'] = False
    
    serializer = CustomUserSerializer(data = request.data)
    if (serializer.is_valid()):
      user = serializer.save()
      token_code = CustomUser.objects.filter(email = email).first().token_code
      if user:
        html_message = render_to_string('email/index.html', {'token_code': token_code})
        email_message = EmailMessage(
          '[VegMarket] - Account Confirmation',
          html_message,
          settings.EMAIL_HOST_USER,
          [email]
        )
        email_message.fail_silently = False
        email_message.content_subtype = 'html'
        email_message.send()
        return Response({'detail':'User created successfully'}, status = status.HTTP_201_CREATED)
      return Response({'detail': 'User created successfully, but failed to send confirmation code'}, status = status.HTTP_206_PARTIAL_CONTENT)
    return Response({'detail':serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
  
  def patch(self, request, format = 'json'):
    jwt_token = request.COOKIES.get('jwt')
    
    if jwt_token is None:
      raise NotAuthenticated('Unauthenticated')
    
    try:
      payload = jwt.decode(jwt_token, 'secret', algorithms = ["HS256"])
    except jwt.ExpiredSignatureError:
      raise NotAuthenticated('Wrong JWT authentication code')
    
    user = CustomUser.objects.filter(id = payload['id']).first()
    serializer = CustomUserSerializer(user, data = request.data, partial = True)
    
    if ('is_staff' in request.data) or ('is_active' in request.data) or ('start_date' in request.data) or ('id' in request.data):
      raise PermissionDenied('You are not allowed to update this field')
    
    if serializer.is_valid():
      serializer.save()
      return Response({'detail': 'User updated successfully'}, status = status.HTTP_202_ACCEPTED)
    return Response ({'detail': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request, format = 'json'):
    jwt_token = request.COOKIES.get('jwt')
    
    if jwt_token is None:
      raise NotAuthenticated('Unauthenticated')
    
    try:
      payload = jwt.decode(jwt_token, 'secret', algorithms = ["HS256"])
    except jwt.ExpiredSignatureError:
      raise NotAuthenticated('Wrong JWT authentication code')
    
    user = CustomUser.objects.filter(id = payload['id']).first()
    
    if user:
      user.delete()
      return Response({'detail': 'User deleted successfully'}, status = status.HTTP_200_OK)
    return Response({'detail': 'User not found'}, status = status.HTTP_404_NOT_FOUND)  
    
class LoginView(APIView):
  def post(self, request, format = 'json'): 
    auth_token = request.headers.get('Authorization', None)
    
    if auth_token is None:
      raise PermissionDenied('No authorization token was provided')
    
    if auth_token != config('AUTHORIZATION_TOKEN'):
      raise PermissionDenied('Wrong authorization token')
    
    if 'email' not in request.data:
      raise ValidationError({'detail':'Email is required'})
    
    email = request.data['email']
    
    if 'password' not in request.data:
      raise ValidationError({'detail':'Password is required'})
    
    password = request.data['password']
    
    user = CustomUser.objects.filter(email = email).first()
    
    if user is None:
      raise AuthenticationFailed('User not found')
    
    if not user.check_password(password):
      raise AuthenticationFailed('Incorrect password')
    
    payload = {
      'id': user.id,
      'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
      'iat': datetime.datetime.utcnow()
    }
    
    user.last_login = datetime.datetime.utcnow()
    user.save()
    
    token = jwt.encode(payload, 'secret', algorithm= 'HS256')
    
    response = Response()
    
    response.set_cookie(key = 'jwt', value = token, httponly = True)
    
    response.data = {'detail':'Token successfully created'}
    
    return response
  
class ActivateAccountView(APIView):
  def get(self, request, format = 'json'):
    jwt_token = request.COOKIES.get('jwt')
    
    if jwt_token is None:
      raise NotAuthenticated('Unauthenticated')
    
    try:
      payload = jwt.decode(jwt_token, 'secret', algorithms = ["HS256"])
    except jwt.ExpiredSignatureError:
      raise NotAuthenticated('Wrong JWT authentication code')
    
    user = CustomUser.objects.filter(id = payload['id']).first()
    
    if not user:
      raise ValidationError({'detail': 'User not found'})
    
    if user.is_active:
      raise ValidationError({'detail': 'User already active'})
    
    token_code = user.token_code
    
    return Response({'detail': token_code})
  
  
  def post(self, request, format = 'json'):
    jwt_token = request.COOKIES.get('jwt')
    
    if jwt_token is None:
      raise NotAuthenticated('Unauthenticated')
    
    try:
      payload = jwt.decode(jwt_token, 'secret', algorithms = ["HS256"])
    except jwt.ExpiredSignatureError:
      raise NotAuthenticated('Wrong JWT authentication code')
    
    user = CustomUser.objects.filter(id = payload['id']).first()
    
    if not user:
      raise ValidationError({'detail': 'User not found'})
    
    if user.is_active:
      raise ValidationError({'detail': 'User already active'})
    
    if 'token_code' not in request.data:
      raise ValidationError({'detail': 'Token code was not provided'})
    
    token_code = request.data['token_code']

    if token_code != user.token_code:
      raise ValidationError({'detail': 'Invalid token code'})
    
    user.is_active = True
    user.is_staff = False
    user.save()
    
    response = Response()
    
    response.data = {'detail': 'User activated successfull'}
    
    return response