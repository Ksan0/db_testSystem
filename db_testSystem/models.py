# coding: utf-8
from django.contrib.auth.models import User
from django.db import models


class RK(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True)
    
    is_active = models.BooleanField(default=False, verbose_name='Открыт')
    registered_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    description = models.TextField(verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Правильный SQL запрос')

    rk = models.ForeignKey(RK, null=True, blank=True, verbose_name='Тест')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    registered_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Attempt(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь')
    rk = models.ForeignKey(RK, verbose_name='Тест')
    used = models.SmallIntegerField(default=0, verbose_name='Использовано попыток')

    def __unicode__(self):
        return u'{0} <-> {1}'.format(self.user.username, self.rk.title)

    class Meta:
        verbose_name = 'Попытка пользователя'
        verbose_name_plural = 'Попытки пользователей'

class UserSession(models.Model):
    user = models.ForeignKey(User)  # относится к юзеру
    rk = models.ForeignKey(RK)  # относится к РК
    attempt = models.SmallIntegerField()  # относится к попытке номер X

    running = models.BooleanField(default=True)
    registered_at = models.DateTimeField(auto_now_add=True)


class SessionQuestions(models.Model):
    session = models.ForeignKey(UserSession)
    question = models.ForeignKey(Question)
    last_answer = models.CharField(max_length=2000)
    is_right = models.BooleanField(default=False)
