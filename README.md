TODO:
============
##Moroz:
- правки для юзера:
  - (В течении 2х дней)если юзер зашел на страницу вопроса и как-то изменил ответ, но не отправил его (кнопкой "отправить ответ"), нужно при попытке сменить/выйти со страницы выводить окошко "вы уверены, что хотите покинуть страницу? Не сохраненные результаты будут утеряны"
- правки для админа:
- разработка:
  - Прикрутить админу к окну панель инструментов:
    - быстро добавить попытки юзеру
  - создавать таблицы из json (текущий вариант снова начал багаться, но на другой таблице)

##Ksan:
- статистика
  - по рк (в перспективе)
  - по вопросу
- рефакторинг
  - редиректить (не оставлять ссылок вроде /restore_password/ или не соответствующих возвращаемой странице)
  - вывод сообщения пользователю (переработать механизм отправки и вывода в шаблон)
  - переработать систему ссылок и их вывод в шаблон
  - password restore: localhost -> domain
- Wiki
  - Задокументировать формат результата выполнения sql  
  - Инструкция по разворачиванию в бой

Testing
============
##Moroz:

##Ksan:
-Закончил тест, но начать новый не смог. Попробовать повторить

Complete
============

##Moroz:
- если попыток не осталось измени заголовок (скрин вк)
- "проверить код" - показать Syntax error, если таковая была


##Ksan:
- sql_query_error должен быть в ' '. Все кавычки внутри должны быть экранированы.
