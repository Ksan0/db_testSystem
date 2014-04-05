# coding: utf-8
from django.contrib.auth.models import User
from django.db import models
from settings_system import *
from subsystems.db_raw_sql_works.DB import Review
import json
from subsystems.index.classes import CustomJSONEncoder


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
    used = models.SmallIntegerField(default=0)
    have = models.SmallIntegerField(default=ATTEMPTES_MAX, verbose_name='Попыток осталось')

    def __unicode__(self):
        return u'{0} <-> {1}'.format(self.user.username, self.rk.title)

    class Meta:
        verbose_name = 'Использованные попытки'
        verbose_name_plural = 'Использованные попытки'


class UserSession(models.Model):
    user = models.ForeignKey(User)  # относится к юзеру
    rk = models.ForeignKey(RK)  # относится к РК
    attempt = models.SmallIntegerField()  # относится к попытке номер X

    running = models.BooleanField(default=True)  # is session running right now?
    registered_at = models.DateTimeField(auto_now_add=True)


class SessionQuestions(models.Model):
    session = models.ForeignKey(UserSession)
    question = models.ForeignKey(Question)
    last_answer = models.CharField(max_length=2000)
    is_right = models.BooleanField(default=False)

    def get_right_records(self):
        if self.question.answer == '':
            msg = {'sql_query_error': 'empty query'}
        else:
            reviewer = Review(right_sql_query=self.question.answer)
            if reviewer.error:
                msg = {'sql_query_error': reviewer.error}
            else:
                msg = reviewer.right_records
        return json.dumps(msg, cls=CustomJSONEncoder)

    def get_user_records(self):
        if self.last_answer == '':
            msg = {'sql_query_error': 'empty query'}
        else:
            reviewer = Review(sql_query=self.last_answer)
            if reviewer.error:
                msg = {'sql_query_error': reviewer.error}
            else:
                msg = reviewer.user_records
        return json.dumps(msg, cls=CustomJSONEncoder)
