from django.forms import *


class LoginForm(forms.Form):
    login = CharField()
    password = CharField(widget=PasswordInput())


class PassRestoreForm(forms.Form):
    login = CharField()


class AnswerForm(forms.Form):
    answer = CharField(widget=Textarea())

    def set_value(self, text):
        self.data['answer'] = text