# coding: utf-8
from django.conf.urls import patterns
from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms import forms
from django.http import HttpResponseRedirect
from models import *


admin.site.unregister(User)
admin.site.unregister(Group)


class UserStatisticInline(admin.StackedInline):
    model = User
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        sessions = UserSession.objects.filter(user=obj)

        self.object = sessions
        return super(UserStatisticInline, self).get_formset(request, obj, **kwargs)


class AttemptInline(admin.TabularInline):
    model = Attempt
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        self.object = Attempt.objects.filter(user=obj)
        return super(AttemptInline, self).get_formset(request, obj, **kwargs)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_active')
    list_editable = ('is_active',)
    fields = ('username', 'first_name', 'last_name', 'is_active')
    inlines = [AttemptInline, UserStatisticInline]

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #    return HttpResponseRedirect('/abc')
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


admin.site.register(Attempt)
admin.site.register(UserSession)
admin.site.register(SessionQuestions)