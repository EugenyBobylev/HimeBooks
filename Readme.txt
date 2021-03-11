# Запустить отладочный сервергыукы
flask run

# Запустить интерпретатор Python в контексте приложения
flask shell

# Выполнить инициализацию БД
flask db init

# создать сценарий миграции
flask db migrate -m "users table"

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
