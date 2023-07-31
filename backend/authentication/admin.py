
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
  add_form = CustomUserCreationForm
  form = CustomUserChangeForm
  readonly_fields = ['start_date', 'token_code', 'last_login']
  list_display = ('email', 'age', 'phone', 'is_active', 'is_staff')

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

# Register the CustomUser model with the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)