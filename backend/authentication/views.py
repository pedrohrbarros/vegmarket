from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from rest_framework import permissions
from .models import CustomUser
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, NotAuthenticated
import jwt, datetime
from decouple import config

class CustomUserView(APIView):
  def get(self, request, format = 'json'):
    jwt_token = request.COOKIES.get('jwt')
    auth_token = request.headers.get('Authorization')
    
    if not auth_token:
      raise PermissionDenied('No authorization token was provided')
    
    if auth_token != config('AUTHORIZATION_TOKEN'):
      raise PermissionDenied('Wrong authorization token')
    
    if not jwt_token:
      raise NotAuthenticated('Unauthenticated')
    
    try:
      payload = jwt.decode(jwt_token, 'secret', algorithms = ["HS256"])
    except jwt.ExpiredSignatureError:
      raise NotAuthenticated("Authentication token has expired")
    
    user = CustomUser.objects.filter(id = payload['id']).first()
    
    serializer = CustomUserSerializer(user)
    
    return Response(serializer.data)
    
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]
  
  def post(self, request): 
    email = request.data['email']
    password = request.data['password']
    user = CustomUser.objects.filter(email = email).first()
    
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