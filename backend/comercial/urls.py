from django.urls import path, re_path
from .views import CategoryListView, CategoryView, ProductListView, ProductView

urlpatterns = [
  path('categories/', CategoryListView.as_view(), name="Category List"),
  re_path(r'^category/(?P<id>.+)/$', CategoryView.as_view(), name = "Category"),
  path('products/', ProductListView.as_view(), name="Product List"),
  re_path(r'^product/(?P<id>.+)/$', ProductView.as_view(), name = "Product")
]