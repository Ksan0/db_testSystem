# coding: utf-8
from django.contrib.auth.models import User
from django.db import models
from settings_system import *
from subsystems.db_raw_sql_works.DB import Review
import json
import re
from subsystems.index.classes import CustomJSONEncoder


class UserExtraInfo(models.Model):
    user = models.ForeignKey(User)
    tech_id = models.IntegerField()


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

    def description_html(self):
        return self.description.replace('\n', '<br/>')


class QuestionType(models.Model):
    title = models.CharField(max_length=250)
    signature = models.CharField(max_length=30)

    def __unicode__(self):
        return self.title

    def isSQLQuery(self):
        return self.signature == 'SQL_query'

    def isTestMultianswer(self):
        return self.signature == 'Test_multianswer' \
                                 ''

class Question(models.Model):
    type = models.ForeignKey(QuestionType, null=True, blank=True, verbose_name='Тип')
    description = models.TextField(verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')

    rk = models.ForeignKey(RK, null=True, blank=True, verbose_name='Тест')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    registered_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def get_records(self):
        if self.type.isSQLQuery():
            reviewer = Review()
            back = reviewer.select(self.answer)
            if back['error']:
                msg = {'sql_query_error': back['error']}
            else:
                msg = back['records']
            return json.dumps(msg, cls=CustomJSONEncoder)
        elif self.type.isTestMultianswer():
            strs = self.get_multianswer_strings()
            bools = self.get_multianswer_bools()
            res = []
            for i in range(len(strs)):
                s = strs[i]
                b = ''
                if bools[i]:
                    b = '+'
                res.append([s, b])
            return json.dumps(res)

    def description_html(self):
        return self.description.replace('\n', '<br/>')

    def answer_html(self):
        return self.answer.replace('\n', '<br/>')

    def get_multianswer_strings(self):
        result = []
        for str in self.answer.split('\n'):
            str_nospace = str.replace(' ', '')
            if len(str_nospace) == 0:
                continue
            if str_nospace.find('++') == 0:
                str = str.replace('++', '', 1)
            result.append(str)
        return result

    def get_multianswer_bools(self):
        result = []
        for str in self.answer.split('\n'):
            str_nospace = str.replace(' ', '')
            if len(str_nospace) == 0:
                continue
            result.append(str_nospace.find('++') == 0)
        return result


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
        return self.question.get_records()

    def get_user_records(self):
        if self.question.type.isSQLQuery():
            reviewer = Review()
            back = reviewer.select(self.last_answer)
            if back['error']:
                msg = {'sql_query_error': back['error']}
            else:
                msg = back['records']
            return json.dumps(msg, cls=CustomJSONEncoder)
        elif self.question.type.isTestMultianswer():
            strs = self.question.get_multianswer_strings()
            bools = self.last_answer
            res = []
            for i in range(len(strs)):
                s = strs[i]
                b = ''
                try:
                    if bools[i] == '1':
                        b = '+'
                except:
                    pass
                res.append([s, b])
            return json.dumps(res)

    def check(self):
        if self.question.type.isSQLQuery():
            reviewer = Review()
            back = reviewer.check_results(sql_query_right=self.question.answer, sql_query_user=self.last_answer)
            self.is_right = back['is_equal']
        elif self.question.type.isTestMultianswer():
            bools = self.question.get_multianswer_bools()
            bools_str = ''
            for b in bools:
                if b:
                    bools_str += '1'
                else:
                    bools_str += '0'
            self.is_right = bools_str == self.last_answer
        self.save()

    def last_answer_html(self):
        if self.question.type.isSQLQuery():
            return self.last_answer.replace('\n', '<br/>')
        elif self.question.type.isTestMultianswer():
            res = ''
            for i in range(len(self.last_answer)):
                if self.last_answer[i] == '1':
                    res += '{0}. + <br/>'.format(i+1)
            return res