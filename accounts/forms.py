from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']
    
    def save(self):
        user = super().save()
        user.is_active = False
        user.save()
        return user


class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]
