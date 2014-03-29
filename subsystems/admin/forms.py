from django.forms import *


class UserForm(forms.Form):
    login = CharField()


class QuestionForm(forms.Form):
    def __init__(self, title, description, answer, rk_choices):
        self.title = CharField(max_length=250, value=title)
        self.description = CharField(value=description, widget=Textarea)
        self.answer = CharField(max_length=2000, value=answer, widget=Textarea)
        self.rk = ChoiceField(choices=rk_choices)


class RKForm(forms.Form):
    def __init__(self, title, description):
        self.title = CharField(max_length=250, value=title)
        self.description = CharField(value=description, widget=Textarea)