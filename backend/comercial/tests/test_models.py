from django.test import TestCase
from comercial.models import Product, Category

class TestModels(TestCase):
    
  def testCreateProduct(self):
    self.category1 = Category.objects.create(
      name = 'Personal Care'
    )
    self.product1 = Product.objects.create(
      name = 'Charcoal-Based Soap',
      description = 'A cleansing and detoxifying soap made with activated charcoal to draw out impurities and leave the skin feeling refreshed.',
      price = 6.99,
      category = self.category1
    )
    self.category2 = Category.objects.create(
      name = "Fashion"
    ),
    self.product2 = Product.objects.create(
      name = 'Vegan Leather Handbag',
      description = 'A stylish handbag made from high-quality synthetic leather that is cruelty-free and environmentally friendly.',
      price = 5999.99,
      category = self.category2
    )