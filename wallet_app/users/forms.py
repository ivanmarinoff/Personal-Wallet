# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
#
#
# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

from django.contrib.auth import forms as auth_forms, get_user_model
from django import template

register = template.Library()

UserModel = get_user_model()


class RegisterUserForm(auth_forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__clear_fields_helper_text()

        for field_name in ['username', 'email', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    def __clear_fields_helper_text(self):
        for field in self.fields.values():
            field.help_text = None
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }


class LoginUserForm(auth_forms.AuthenticationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'password')
        labels = {
            'username': 'Username',
            'password': 'Password',
        }


@register.filter
def form_field_class(form_field, className):
    default_classname = form_field.field.widget.attrs.get('class', '')
    form_field.field.widget.attrs['class'] = default_classname + ' ' + className
    return form_field
