# создать новую ветку и переключиться
$ git branch iss53
$ git checkout iss53
# или сокращенно
$ git checkout -b iss53

# Запустить отладочный сервер
flask run

# Запустить интерпретатор Python в контексте приложения
flask shell

# Выполнить инициализацию БД
flask db init

# создать сценарий миграции
flask db migrate -m "books table"

# применить изменения к БД
flask db upgrade

# Отменить последнее обновление БД
flask db downgrade


# Установить значение переменной окружения
export FLASK_APP='homebooks.py'

# Вкл. режим отладки
export FLASK_DEBUG = 1

# Просмотреть значение указанной переменной окружения
printenv FLASK_APP

# Эээээээ что-то с работой .env , .flaskenv
pip install python-dotenv
