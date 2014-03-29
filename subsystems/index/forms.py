from django.forms import *


class LoginForm(forms.Form):
    login = CharField()
    password = CharField(widget=PasswordInput())


class AnswerForm(forms.Form):
    answer = CharField(widget=Textarea())