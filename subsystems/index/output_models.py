from db_testSystem.models import *
from db_testSystem.settings_system import *


class OutputRKModel(RK):
    def __init__(self, sup, user):
        self.id = sup.id
        self.title = sup.title
        self.description = sup.description

        try:
            self.attemptes_amount = Attempt.objects.get(user=user, rk=sup).have
        except:
            self.attemptes_amount = ATTEMPTES_MAX


class OutputQuestionModel(Question):
    def __init__(self, sup, status):
        self.id = sup.id
        self.description = sup.description
        self.status = status

    def __unicode__(self):
        return "id={0}, descr={1}, status={2}".format(self.id, self.description, self.status)