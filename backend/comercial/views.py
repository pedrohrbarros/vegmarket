from rest_framework.views import APIView
from rest_framework.exceptions import NotAuthenticated, NotFound, ValidationError, PermissionDenied
import jwt
from .serializers import CategorySerializer, ProductSerializer
from .models import Category, Product
from rest_framework.response import Response
from rest_framework import status

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
  
  def post(self, request, format = 'json'):
    jwt_token = request.COOKIES.get('jwt', None)
    
    if jwt_token is None:
      raise NotAuthenticated({'detail':'Unauthenticated'})
    
    try:
      jwt.decode(jwt_token, 'secret', algorithms = ["HS256"])
    except jwt.ExpiredSignatureError:
      raise NotAuthenticated({'detail':'Wrong JWT authentication code'})
    
    if 'name' not in request.data:
      raise ValidationError({'detail': 'Name is required'})
    
    serializer = CategorySerializer(request.data)
    
    if serializer.is_valid():
      serializer.save()
      return Response({'detail': 'Category successfully created'}, status = status.HTTP_201_CREATED)
    return Response({'detail': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
  
  def patch(self, request, format = 'json' , *args, **kwargs):
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
    
    serializer = CategorySerializer(category, data = request.data, partial = True)
    
    if 'id' in request.data:
      raise PermissionDenied('Your are not allowed to update this field')
    
    if serializer.is_valid():
      serializer.save()
      return Response({'detail': 'Category updated successfully'}, status = status.HTTP_202_ACCEPTED)
    return Response({'detail': serializer.erros}, status = status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request, format = 'json', *args, **kwargs):
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
    
    category.delete()
    return Response({'detail': 'Category deleted successfully'})
  
class ProductListView(APIView):
  def get(self, request, format = 'json'):
    jwt_token = request.COOKIES.get('jwt', None)
    
    if jwt_token is None:
      raise NotAuthenticated({'detail':'Unauthenticated'})
    
    try:
      jwt.decode(jwt_token, 'secret', algorithms = ["HS256"])
    except jwt.ExpiredSignatureError:
      raise NotAuthenticated({'detail':'Wrong JWT authentication code'})
    
    product_list = Product.objects.all()
    serializer = ProductSerializer(product_list, many = True)
    return Response(serializer.data)
  
class ProductView(APIView):
  def get(self, request, format = 'json', *args, **kwargs):
    jwt_token = request.COOKIES.get('jwt', None)
    
    if jwt_token is None:
      raise NotAuthenticated({'detail':'Unauthenticated'})
    
    try:
      jwt.decode(jwt_token, 'secret', algorithms = ["HS256"])
    except jwt.ExpiredSignatureError:
      raise NotAuthenticated({'detail':'Wrong JWT authentication code'})
    
    id = self.kwargs['id']
    product = Product.objects.filter(id = id).first()
    
    if not product:
      raise NotFound({'detail':'No product found for this ID'})
    
    serializer = ProductSerializer(product)
    return Response(serializer.data)
  
  def post(self, request, format = 'json'):
    jwt_token = request.COOKIES.get('jwt', None)
    
    if jwt_token is None:
      raise NotAuthenticated({'detail':'Unauthenticated'})
    
    try:
      jwt.decode(jwt_token, 'secret', algorithms = ["HS256"])
    except jwt.ExpiredSignatureError:
      raise NotAuthenticated({'detail':'Wrong JWT authentication code'})
    
    if 'name' not in request.data:
      raise ValidationError({'detail': 'Name is required'})
    
    serializer = ProductSerializer(request.data)
    
    if serializer.is_valid():
      serializer.save()
      return Response({'detail': 'Product successfully created'}, status = status.HTTP_201_CREATED)
    return Response({'detail': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
  
  def patch(self, request, format = 'json' , *args, **kwargs):
    jwt_token = request.COOKIES.get('jwt', None)
    
    if jwt_token is None:
      raise NotAuthenticated({'detail':'Unauthenticated'})
    
    try:
      jwt.decode(jwt_token, 'secret', algorithms = ["HS256"])
    except jwt.ExpiredSignatureError:
      raise NotAuthenticated({'detail':'Wrong JWT authentication code'})
    
    id = self.kwargs['id']
    product = Product.objects.filter(id = id).first()
    
    if not product:
      raise NotFound({'detail':'No product found for this ID'})
    
    serializer = ProductSerializer(product, data = request.data, partial = True)
    
    if 'id' in request.data:
      raise PermissionDenied('Your are not allowed to update this field')
    
    if serializer.is_valid():
      serializer.save()
      return Response({'detail': 'Product updated successfully'}, status = status.HTTP_202_ACCEPTED)
    return Response({'detail': serializer.erros}, status = status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request, format = 'json', *args, **kwargs):
    jwt_token = request.COOKIES.get('jwt', None)
    
    if jwt_token is None:
      raise NotAuthenticated({'detail':'Unauthenticated'})
    
    try:
      jwt.decode(jwt_token, 'secret', algorithms = ["HS256"])
    except jwt.ExpiredSignatureError:
      raise NotAuthenticated({'detail':'Wrong JWT authentication code'})
    
    id = self.kwargs['id']
    product = Product.objects.filter(id = id).first()
    
    if not product:
      raise NotFound({'detail':'No product found for this ID'})
    
    product.delete()
    return Response({'detail': 'Product deleted successfully'})