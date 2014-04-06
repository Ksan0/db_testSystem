# coding: utf-8


class UserMessage():
    def __init__(self, msg=None):
        self.dict_success = {
            'confirm_success': 'Восстановление прошло успешно, пароль отправлен на почту',
            'look_at_mail': 'Проверьте вашу почту',
        }
        self.dict_warning = {
        }
        self.dict_error = {
            'confirm_failed': 'Не удалось восстановить пароль',
            'no_user': 'Такого пользователя не существует',
            'no_time': 'Время вышло',
            'no_attemptes': 'Не хватает попыток',
            'session_closed': 'Вы уже закончили сессию',
            'login_failed': 'Извините вы ошиблись с логином или паролем',
            'disabled_user': 'Юзер неактивен',
            'another_test_running': 'Вы уже выполняете тест, завершите, чтобы начать следующий'
        }

        if msg in self.dict_success:
            self.msg = self.dict_success[msg]
            self.type = 'success'
        elif msg in self.dict_warning:
            self.msg = self.dict_warning[msg]
            self.type = 'warning'
        elif msg in self.dict_error:
            self.msg = self.dict_error[msg]
            self.type = 'error'
        else:
            raise Exception('Unknown user message')

    def message(self):
        return self.msg

    def type(self):
        return self.type