from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.password_validation import (
    CommonPasswordValidator,
    MinimumLengthValidator,
    NumericPasswordValidator,
    UserAttributeSimilarityValidator,
)
import random
import string

class CustomAccountManager(BaseUserManager):
  def create_superuser(self, email, password, **other_fields):
    other_fields.setdefault('is_staff', True)
    other_fields.setdefault('is_superuser', True)
    other_fields.setdefault('is_active', True)
    
    if other_fields.get('is_staff') is not True:
      raise ValueError('Superuser must be assigned to is_staff = True')
    
    if other_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must be assigned to is_superuser = True')
    
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
      raise ValueError('\n'.join(password_validation_errors))
    
    return self.create_user(email, password, **other_fields)
  
  def create_user(self, email, password, is_staff, is_active, **other_fields):
    if not email:
      raise ValueError('E-mail adress must be provided')
    
    if not password:
      raise ValueError('Password must be provided')
    
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
      raise ValueError('\n'.join(password_validation_errors))
    
    email = self.normalize_email(email)
    user = self.model(
      email = email,
      is_staff = is_staff,
      is_active = is_active,
      **other_fields
    )
    
    user.set_password(password)
    
    user.save()
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
  id = models.AutoField(primary_key = True)
  name = models.CharField(verbose_name = "Name", max_length = 255, blank = True, null = True)
  email = models.EmailField(verbose_name = "E-mail Adress", unique = True, null = False, blank = False)
  password = models.CharField(verbose_name = "Password", max_length = 255, blank = False, null = False)
  name = models.CharField(verbose_name = "Name", max_length = 150, blank = False, unique = False, null = False)
  phone = models.CharField(verbose_name = "Phone Number", max_length = 21, blank = True, null = True)
  age = models.IntegerField(default = 0, verbose_name = "Age")
  token_code = models.CharField(verbose_name = "Auth Token Code", max_length = 16, blank = True, null = True)
  start_date = models.DateTimeField(default = timezone.now, null = False, blank = False)
  is_active = models.BooleanField(verbose_name = "Is Active?", default = False)
  is_staff = models.BooleanField(verbose_name = "Is Staff?", default = False)
  
  objects = CustomAccountManager()
  
  USERNAME_FIELD = 'email'
  
  def generate_random_token(self):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
  
  def save(self, *args, **kwargs):
    self.token_code = self.generate_random_token()
    super(CustomUser, self).save(*args, **kwargs)
    
  def __str__(self):
    return self.name
  
  class Meta:
    verbose_name_plural = 'Custom User'
  