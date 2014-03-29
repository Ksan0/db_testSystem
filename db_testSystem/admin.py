# coding: utf-8
from django.contrib import admin
from django.contrib.auth.models import Group
from models import *


admin.site.unregister(User)
admin.site.unregister(Group)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_active')
    list_editable = ('is_active',)
    fields = ('username', 'password', 'first_name', 'last_name', 'is_active')
admin.site.register(User, UserAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'rk', 'is_active')
    list_editable = ('rk', 'is_active')
    list_filter = ('rk',)
admin.site.register(Question, QuestionAdmin)


class RKAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_editable = ('is_active',)
admin.site.register(RK, RKAdmin)


class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'rk', 'used')
    list_editable = ('used',)
admin.site.register(Attempt, AttemptAdmin)