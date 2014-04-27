from db_testSystem.models import *
from db_testSystem.settings_system import *


class OutputRKModel():
    def __init__(self, sup, user):  # sup = rk
        self.id = sup.id
        self.title = sup.title
        self.description = sup.description
        self.is_active = sup.is_active

        best_result = 0
        try:
            attempt = Attempt.objects.get(user=user, rk=sup)
            self.attemptes_amount = attempt.have

            # rk, attempt_number, que_count_all, que_count_right
            for i in xrange(1, attempt.used+1):
                try:
                    session = UserSession.objects.get(user=user, rk=attempt.rk, attempt=i)
                    session_ques = SessionQuestions.objects.filter(session=session)
                    if session_ques.filter(is_right=True).count() > best_result:
                        best_result = session_ques.filter(is_right=True).count()
                except:
                    pass
        except:
            self.attemptes_amount = ATTEMPTES_MAX

        self.best_result = best_result * QUESTION_WEIGHT



class OutputQuestionModel():
    def __init__(self, sup, status):
        self.id = sup.id
        self.description = sup.description
        self.status = status

    def __unicode__(self):
        return "id={0}, descr={1}, status={2}".format(self.id, self.description, self.status)