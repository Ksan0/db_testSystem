from django.forms import *


class LoginForm(forms.Form):
    login = CharField()
    password = CharField(widget=PasswordInput())