from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
      model = CustomUser
      fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude the password field if it's not changed
        if not self.instance.pk:
            self.fields.pop('password')

    def clean_password(self):
        # Return the existing password if the field is not changed
        return self.initial.get('password', self.cleaned_data.get('password'))