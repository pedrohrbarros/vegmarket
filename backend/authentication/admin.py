
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.password_validation import (
    CommonPasswordValidator,
    MinimumLengthValidator,
    NumericPasswordValidator,
    UserAttributeSimilarityValidator,
)
from django import forms

class CustomUserAdmin(UserAdmin):
  add_form = CustomUserCreationForm
  form = CustomUserChangeForm
  readonly_fields = ['start_date', 'token_code', 'last_login']
  list_display = ('name', 'age', 'phone', 'is_active', 'is_staff')

  # Use 'email' instead of 'username' for user lookups
  fieldsets = (
    ('Authentication',
     {'fields': 
       ('email', 'password')
      }),
    ('Personal Information',
     {'fields':
       ('name', 'phone', 'age')
      }),
    ('Permissions',
     {'fields': 
       ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
      }),
    ('Important dates',
     {'fields':
       ('last_login', 'start_date')
      }),
  )
  add_fieldsets = (
    (None, 
     {
        'classes': ('wide',),
        'fields': ('email', 'password1', 'password2'),
      }
    ),
  )
  list_filter = ('is_staff', 'is_superuser', 'is_active')
  search_fields = ('email',)
  ordering = ('email',)
  
  def get_queryset(self, request):
    # Limit regular users to see only their own profile, not all users
    qs = super().get_queryset(request)
    if not request.user.is_superuser:
      qs = qs.filter(pk=request.user.pk)
    return qs
  # Use 'email' instead of 'username' for user lookups
  def get_user(self, user_id):
    try:
      return CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
      return None
    
  def formfield_for_password(self, db_field, request, **kwargs):
    # Apply password strength validation during user password changes
    if db_field.name == 'password':
      kwargs['widget'] = forms.PasswordInput(attrs={'autocomplete': 'new-password'})
      password_validators = [
        MinimumLengthValidator(),
        CommonPasswordValidator(),
        NumericPasswordValidator(),
        UserAttributeSimilarityValidator()
      ]
      password_validation_errors = []
      for validator in password_validators:
        try:
          validator.validate(None, password=self.instance.password)
        except Exception as e:
          password_validation_errors.extend(e.messages)
      if password_validation_errors:
        kwargs['help_text'] = "\n".join(password_validation_errors)

    return super().formfield_for_password(db_field, request, **kwargs)
  
  def get_fieldsets(self, request, obj=None):
    # Customize fieldsets based on the user's superuser status
    fieldsets = super().get_fieldsets(request, obj)
    if not request.user.is_superuser:
      # If the user is not a superuser, remove the specified fields from fieldsets
      for fieldset in fieldsets:
        fieldset[1]['fields'] = tuple(field for field in fieldset[1]['fields'] if field not in ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'))
    return fieldsets

# Register the CustomUser model with the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)