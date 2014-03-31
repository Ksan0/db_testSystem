from db_testSystem.models import *

class UserSessionOutputModel():
    def __init__(self, user_session):
        self.session = user_session
        self.session_questions = SessionQuestions.objects.filter(session=user_session)
        self.questions_right_count = self.session_questions.filter(is_right=True).count()
        self.questions_all_count = self.session_questions.count()