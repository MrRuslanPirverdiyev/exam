from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import requests
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Модели базы данных
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    display_name = db.Column(db.String(80), unique=True, nullable=False)
    total_score = db.Column(db.Integer, default=0)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(500), nullable=False)
    option1 = db.Column(db.String(200), nullable=False)
    option2 = db.Column(db.String(200), nullable=False)
    option3 = db.Column(db.String(200), nullable=False)
    option4 = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False)  # 1, 2, 3, или 4

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Главная страница с погодой
@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    city = None
    error = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            try:
                # Используем OpenWeatherMap API (нужен API ключ)
                # Для демонстрации используем заглушку
                API_KEY = os.environ.get('WEATHER_API_KEY', 'demo')
                
                if API_KEY == 'demo':
                    # Демо-данные для разработки
                    weather_data = generate_demo_weather(city)
                else:
                    # Реальный запрос к API
                    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ru'
                    response = requests.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        weather_data = parse_weather_data(data)
                    else:
                        error = 'Город не найден'
            except Exception as e:
                error = f'Ошибка получения данных о погоде: {str(e)}'
    
    return render_template('index.html', weather_data=weather_data, city=city, error=error)

def generate_demo_weather(city):
    """Генерирует демо-данные погоды для разработки"""
    days = ['Понедельник', 'Вторник', 'Среда']
    dates = ['01.12.2025', '02.12.2025', '03.12.2025']
    weather = []
    
    for i in range(3):
        weather.append({
            'day': days[i],
            'date': dates[i],
            'temp_day': random.randint(-5, 10),
            'temp_night': random.randint(-15, 0)
        })
    
    return weather

def parse_weather_data(data):
    """Парсит данные из OpenWeatherMap API"""
    forecast = []
    # Группируем по дням
    days_dict = {}
    
    for item in data['list']:
        date = datetime.fromtimestamp(item['dt'])
        day_key = date.strftime('%Y-%m-%d')
        
        if day_key not in days_dict:
            days_dict[day_key] = {
                'temps': [],
                'date': date
            }
        
        days_dict[day_key]['temps'].append(item['main']['temp'])
    
    # Берем первые 3 дня
    for i, (day_key, day_data) in enumerate(list(days_dict.items())[:3]):
        date = day_data['date']
        temps = day_data['temps']
        
        forecast.append({
            'day': date.strftime('%A'),
            'date': date.strftime('%d.%m.%Y'),
            'temp_day': max(temps),
            'temp_night': min(temps)
        })
    
    return forecast

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        display_name = request.form.get('display_name')
        
        # Валидация
        if not username or not password or not display_name:
            flash('Все поля обязательны для заполнения', 'danger')
            return render_template('register.html')
        
        if password != password_confirm:
            flash('Пароли не совпадают', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Логин уже занят', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(display_name=display_name).first():
            flash('Имя для отображения уже занято', 'danger')
            return render_template('register.html')
        
        # Создание пользователя
        user = User(username=username, display_name=display_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация успешна! Теперь вы можете войти', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('quiz'))
        else:
            flash('Неверный логин или пароль', 'danger')
    
    return render_template('login.html')

# Выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

# Викторина
@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if request.method == 'POST':
        question_id = request.form.get('question_id')
        answer = request.form.get('answer')
        
        question = Question.query.get(question_id)
        
        if question and int(answer) == question.correct_answer:
            current_user.total_score += 1
            db.session.commit()
            result = 'correct'
        else:
            result = 'incorrect'
        
        return jsonify({'result': result, 'new_score': current_user.total_score})
    
    # Получаем случайный вопрос
    questions = Question.query.all()
    if not questions:
        flash('Вопросы еще не добавлены в базу данных', 'warning')
        return render_template('quiz.html', question=None)
    
    question = random.choice(questions)
    return render_template('quiz.html', question=question)

# Таблица лидеров
@app.route('/leaderboard')
def leaderboard():
    leaders = User.query.order_by(User.total_score.desc()).limit(10).all()
    return render_template('leaderboard.html', leaders=leaders)

# Инициализация БД и добавление тестовых вопросов
def init_db():
    with app.app_context():
        db.create_all()
        
        # Добавляем вопросы, если их нет
        if Question.query.count() == 0:
            questions = [
                Question(
                    question_text='Какой язык программирования используется для создания веб-приложений?',
                    option1='Python',
                    option2='Java',
                    option3='C++',
                    option4='Все перечисленные',
                    correct_answer=4
                ),
                Question(
                    question_text='Что такое Flask?',
                    option1='База данных',
                    option2='Веб-фреймворк',
                    option3='Язык программирования',
                    option4='Текстовый редактор',
                    correct_answer=2
                ),
                Question(
                    question_text='Какой HTTP метод используется для отправки формы?',
                    option1='GET',
                    option2='POST',
                    option3='PUT',
                    option4='DELETE',
                    correct_answer=2
                ),
                Question(
                    question_text='Что означает HTML?',
                    option1='HyperText Markup Language',
                    option2='High Tech Modern Language',
                    option3='Home Tool Markup Language',
                    option4='Hyperlinks and Text Markup Language',
                    correct_answer=1
                ),
                Question(
                    question_text='Какой тег используется для создания ссылки в HTML?',
                    option1='<link>',
                    option2='<a>',
                    option3='<href>',
                    option4='<url>',
                    correct_answer=2
                ),
                Question(
                    question_text='Что такое CSS?',
                    option1='Cascading Style Sheets',
                    option2='Computer Style Sheets',
                    option3='Creative Style Sheets',
                    option4='Colorful Style Sheets',
                    correct_answer=1
                ),
                Question(
                    question_text='Какой порт по умолчанию использует HTTP?',
                    option1='443',
                    option2='8080',
                    option3='80',
                    option4='3000',
                    correct_answer=3
                ),
                Question(
                    question_text='Что такое SQL?',
                    option1='Structured Query Language',
                    option2='Simple Question Language',
                    option3='Server Query Language',
                    option4='System Quality Language',
                    correct_answer=1
                ),
            ]
            
            for q in questions:
                db.session.add(q)
            
            db.session.commit()
            print('База данных инициализирована с тестовыми вопросами')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

