# Подробная инструкция по деплою на PythonAnywhere

## Предварительные требования
- Аккаунт на PythonAnywhere (бесплатный)
- Файлы проекта готовы к загрузке

## Пошаговая инструкция

### 1. Регистрация на PythonAnywhere

1. Перейдите на https://www.pythonanywhere.com/
2. Нажмите "Pricing & signup"
3. Выберите "Create a Beginner account" (бесплатно)
4. Заполните форму регистрации
5. Подтвердите email

### 2. Загрузка файлов проекта

#### Вариант А: Через Files (проще)
1. Войдите в PythonAnywhere
2. Перейдите во вкладку "Files"
3. Создайте новую папку, например `quiz_app`
4. Загрузите все файлы проекта через кнопку "Upload a file":
   - app.py
   - requirements.txt
   - Создайте папку `templates` и загрузите в нее все HTML файлы

#### Вариант Б: Через Git (если есть репозиторий)
1. Перейдите во вкладку "Consoles"
2. Запустите "Bash" консоль
3. Выполните команды:
```bash
git clone https://github.com/ваш_username/ваш_репозиторий.git
cd ваш_репозиторий
```

### 3. Установка зависимостей

В консоли Bash выполните:
```bash
cd ~/quiz_app  # или путь к вашей папке
pip3 install --user flask flask-sqlalchemy flask-login flask-wtf requests
```

Или:
```bash
pip3 install --user -r requirements.txt
```

### 4. Инициализация базы данных

В той же консоли:
```bash
python3 app.py
```

Дождитесь сообщения "База данных инициализирована с тестовыми вопросами", затем нажмите Ctrl+C для остановки.

### 5. Настройка Web приложения

1. Перейдите во вкладку "Web"
2. Нажмите "Add a new web app"
3. Нажмите "Next"
4. Выберите "Manual configuration" (НЕ выбирайте Flask!)
5. Выберите Python 3.10 (или последнюю доступную версию)
6. Нажмите "Next"

### 6. Настройка WSGI конфигурации

1. В разделе "Code" найдите строку с "WSGI configuration file"
2. Кликните на путь к файлу (что-то вроде `/var/www/ваш_username_pythonanywhere_com_wsgi.py`)
3. **Удалите ВСЕ** содержимое файла
4. Вставьте следующий код (замените `ваш_username` на ваше имя пользователя):

```python
import sys
import os

# Путь к директории с проектом
path = '/home/ваш_username/quiz_app'
if path not in sys.path:
    sys.path.insert(0, path)

# Импорт приложения
from app import app as application

# Инициализация БД
from app import init_db
init_db()
```

5. Нажмите "Save" (сверху справа)

### 7. Настройка виртуального окружения (опционально, но рекомендуется)

Если вы хотите использовать виртуальное окружение:

В консоли:
```bash
cd ~
mkvirtualenv --python=/usr/bin/python3.10 quiz_env
pip install flask flask-sqlalchemy flask-login flask-wtf requests
```

Затем на странице Web укажите путь к виртуальному окружению:
`/home/ваш_username/.virtualenvs/quiz_env`

### 8. Перезагрузка приложения

1. Вернитесь на вкладку "Web"
2. Прокрутите вверх
3. Нажмите зеленую кнопку "Reload ваш_username.pythonanywhere.com"

### 9. Проверка работы

1. Перейдите по адресу: `https://ваш_username.pythonanywhere.com`
2. Проверьте все функции:
   - Регистрация
   - Вход
   - Викторина
   - Таблица лидеров
   - Виджет погоды

### 10. Настройка API погоды (опционально)

Для реального прогноза погоды:

1. Зарегистрируйтесь на https://openweathermap.org/api
2. Создайте бесплатный API ключ
3. На PythonAnywhere:
   - Перейдите во вкладку "Web"
   - Найдите раздел "Environment variables"
   - Нажмите "Add a new environment variable"
   - Name: `WEATHER_API_KEY`
   - Value: `ваш_api_ключ_с_openweathermap`
4. Нажмите "Reload" для применения изменений

## Возможные проблемы и решения

### Проблема: "ModuleNotFoundError"
**Решение**: Убедитесь, что все пакеты установлены:
```bash
pip3 install --user flask flask-sqlalchemy flask-login flask-wtf requests
```

### Проблема: "500 Internal Server Error"
**Решение**: 
1. Проверьте логи ошибок во вкладке "Web" -> "Log files" -> "Error log"
2. Убедитесь, что пути в WSGI файле указаны правильно
3. Проверьте, что база данных инициализирована

### Проблема: Страницы не загружаются
**Решение**:
1. Убедитесь, что в папке `templates` находятся все HTML файлы
2. Проверьте структуру папок

### Проблема: База данных не создается
**Решение**:
```bash
cd ~/quiz_app
python3
>>> from app import db, app
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

## Важные замечания

1. **Бесплатный аккаунт**: Ограничения бесплатного аккаунта PythonAnywhere:
   - Один веб-сайт
   - Ограниченное CPU время
   - Нужно заходить и перезагружать сайт раз в 3 месяца

2. **Безопасность**: 
   - Измените `SECRET_KEY` в `app.py` на случайную строку
   - Не коммитьте файлы с паролями в публичный репозиторий

3. **Обновление**: Для обновления приложения:
   - Измените файлы через вкладку "Files"
   - Нажмите "Reload" на вкладке "Web"

4. **База данных**: 
   - Файл `quiz.db` создается автоматически при первом запуске
   - Находится в папке с проектом
   - Для сброса БД - удалите `quiz.db` и запустите `python3 app.py` снова

## Полезные ссылки

- Документация PythonAnywhere: https://help.pythonanywhere.com/
- Flask документация: https://flask.palletsprojects.com/
- OpenWeatherMap API: https://openweathermap.org/api

---

Если возникли проблемы - проверьте логи в разделе "Web" -> "Log files"

