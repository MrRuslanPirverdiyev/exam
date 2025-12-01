# Пример WSGI файла для PythonAnywhere
# Скопируйте это содержимое в WSGI configuration file на PythonAnywhere
# Замените 'ваш_username' на ваше имя пользователя

import sys
import os

# Добавьте путь к вашему проекту
# Замените 'ваш_username' на ваше имя пользователя PythonAnywhere
path = '/home/ваш_username/quiz_app'
if path not in sys.path:
    sys.path.insert(0, path)

# Импортируйте приложение Flask
from app import app as application

# Инициализация базы данных при запуске
from app import init_db
init_db()

