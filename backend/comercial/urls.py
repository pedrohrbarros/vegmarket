from django.urls import path, re_path
from .views import CategoryListView, CategoryView

urlpatterns = [
  path('categories/', CategoryListView.as_view(), name="Category List"),
  re_path(r'^category/(?P<id>.+)/$', CategoryView.as_view(), name = "Category")
]