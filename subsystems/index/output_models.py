from db_testSystem.models import *
from db_testSystem.system_settings import *


class OutputRKModel(RK):
    def __init__(self, sup, user):
        self.id = sup.id
        self.title = sup.title
        self.description = sup.description

        try:
            self.attemptes_amount = ATTEMPTES_MAX - Attempt.objects.get(user=user, rk=sup).used
        except:
            self.attemptes_amount = ATTEMPTES_MAX


class OutputQuestionModel(Question):
    def __init__(self, sup, status):
        self.id = sup.id
        self.description = sup.description
        self.status = status