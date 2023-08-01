from django.db import models


def product_directory_path(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / product_<id>/<filename>
    return 'comercial/product_{0}/{1}'.format(instance.product.id, filename)

class Category(models.Model):
  id = models.AutoField(primary_key = True)
  name = models.CharField(max_length = 255, unique = True, blank = False, null = False)
  
  def __str__(self):
    return self.name
  
  class Meta:
    verbose_name_plural = 'Category'

class Product(models.Model):
  id = models.AutoField(primary_key = True)
  name = models.CharField(verbose_name = "Name", max_length = 255, blank = False, null = False)
  description = models.TextField(verbose_name = "Description", blank = False, null = False)
  image = models.ImageField(verbose_name = "Image", upload_to = product_directory_path,blank = False, null = False)
  price = models.DecimalField(verbose_name = "Price", max_digits = 15, decimal_places = 10, null = False, blank = False)
  category = models.ForeignKey(Category, blank = False, null = False, on_delete = models.CASCADE)
  
  def __str__(self):
    return self.name
  
  class Meta:
    verbose_name_plural = 'Product'