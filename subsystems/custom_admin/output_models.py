from db_testSystem.models import *


class UserSessionOutputModel():
    def __init__(self, user_session):
        self.session = user_session
        self.session_questions = SessionQuestions.objects.filter(session=user_session)

        self.questions_right_count = self.session_questions.filter(is_right=True).count()
        self.questions_all_count = self.session_questions.count()

class UserOutputModel(User):
    def __init__(self, user):
        self.user = user

        self.rk = []
        for attempt in Attempt.objects.filter(user=user):
            best_row = (0, 0, 0, 0)
            for i in xrange(1, attempt.used+1):
                session = UserSession.objects.get(user=user, rk=attempt.rk, attempt=i)
                session_ques = SessionQuestions.objects.filter(session=session)
                if session_ques.filter(is_right=True).count() >= best_row[-1]:
                    best_row = (attempt.rk, i, session_ques.count(), session_ques.filter(is_right=True).count())
                # rk, attempt_number, que_count_all, que_count_right
            self.rk.append(best_row)
