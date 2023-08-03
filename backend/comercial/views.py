from rest_framework.views import APIView
from rest_framework.exceptions import NotAuthenticated, NotFound
import jwt
from .serializers import CategorySerializer, ProductSerializer
from .models import Category, Product
from rest_framework.response import Response

class CategoryListView(APIView):
  def get(self, request, format = 'json'):
    jwt_token = request.COOKIES.get('jwt', None)
    
    if jwt_token is None:
      raise NotAuthenticated({'detail':'Unauthenticated'})
    
    try:
      jwt.decode(jwt_token, 'secret', algorithms = ["HS256"])
    except jwt.ExpiredSignatureError:
      raise NotAuthenticated({'detail':'Wrong JWT authentication code'})
    
    category_list = Category.objects.all()
    serializer = CategorySerializer(category_list, many = True)
    return Response(serializer.data)
  
class CategoryView(APIView):
  def get(self, request, format = 'json', *args, **kwargs):
    jwt_token = request.COOKIES.get('jwt', None)
    
    if jwt_token is None:
      raise NotAuthenticated({'detail':'Unauthenticated'})
    
    try:
      jwt.decode(jwt_token, 'secret', algorithms = ["HS256"])
    except jwt.ExpiredSignatureError:
      raise NotAuthenticated({'detail':'Wrong JWT authentication code'})
    
    id = self.kwargs['id']
    category = Category.objects.filter(id = id).first()
    
    if not category:
      raise NotFound({'detail':'No category found for this ID'})
    
    serializer = CategorySerializer(category)
    return Response(serializer.data)