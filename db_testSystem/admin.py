# coding: utf-8
from django.contrib import admin
from django.contrib.auth.models import Group
from models import *


admin.site.unregister(User)
admin.site.unregister(Group)


class NewRKModel(RK):
    def __init__(self):
        self.questions = Question.objects.filter(rk=self)

    class Meta:
        proxy = True

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'rk', 'is_active')
    list_editable = ('rk', 'is_active')
admin.site.register(Question, QuestionAdmin)


class RKAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_editable = ('is_active',)
admin.site.register(NewRKModel, RKAdmin)