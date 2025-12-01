"""
Скрипт для добавления дополнительных вопросов в викторину
Запустите: python add_questions.py
"""

from app import app, db, Question

# Дополнительные вопросы на разные темы
additional_questions = [
    # Вопросы по программированию
    {
        'question_text': 'Какой оператор используется для сравнения в Python?',
        'option1': '=',
        'option2': '==',
        'option3': '===',
        'option4': ':=',
        'correct_answer': 2
    },
    {
        'question_text': 'Что такое JSON?',
        'option1': 'JavaScript Object Notation',
        'option2': 'Java Standard Object Notation',
        'option3': 'JavaScript Online Network',
        'option4': 'Java Script Object Name',
        'correct_answer': 1
    },
    {
        'question_text': 'Какая команда Git используется для клонирования репозитория?',
        'option1': 'git pull',
        'option2': 'git copy',
        'option3': 'git clone',
        'option4': 'git download',
        'correct_answer': 3
    },
    {
        'question_text': 'Что означает API?',
        'option1': 'Application Programming Interface',
        'option2': 'Advanced Programming Integration',
        'option3': 'Automated Program Interaction',
        'option4': 'Application Process Implementation',
        'correct_answer': 1
    },
    {
        'question_text': 'Какой метод HTTP используется для обновления ресурса?',
        'option1': 'GET',
        'option2': 'POST',
        'option3': 'PUT',
        'option4': 'DELETE',
        'correct_answer': 3
    },
    # Вопросы по базам данных
    {
        'question_text': 'Что означает CRUD в разработке?',
        'option1': 'Create, Read, Update, Delete',
        'option2': 'Copy, Read, Use, Delete',
        'option3': 'Create, Remove, Update, Display',
        'option4': 'Connect, Read, Upload, Download',
        'correct_answer': 1
    },
    {
        'question_text': 'Какая база данных является реляционной?',
        'option1': 'MongoDB',
        'option2': 'Redis',
        'option3': 'PostgreSQL',
        'option4': 'Cassandra',
        'correct_answer': 3
    },
    # Вопросы по веб-разработке
    {
        'question_text': 'Какой тег HTML используется для вставки изображения?',
        'option1': '<image>',
        'option2': '<img>',
        'option3': '<picture>',
        'option4': '<photo>',
        'correct_answer': 2
    },
    {
        'question_text': 'Что такое Bootstrap?',
        'option1': 'Язык программирования',
        'option2': 'CSS фреймворк',
        'option3': 'База данных',
        'option4': 'Текстовый редактор',
        'correct_answer': 2
    },
    {
        'question_text': 'Какой селектор CSS выбирает элемент по ID?',
        'option1': '.',
        'option2': '#',
        'option3': '*',
        'option4': '@',
        'correct_answer': 2
    },
    # Общие вопросы по IT
    {
        'question_text': 'Что такое DNS?',
        'option1': 'Domain Name System',
        'option2': 'Data Network Service',
        'option3': 'Digital Name Server',
        'option4': 'Direct Network System',
        'correct_answer': 1
    },
    {
        'question_text': 'Какой порт использует HTTPS по умолчанию?',
        'option1': '80',
        'option2': '443',
        'option3': '8080',
        'option4': '3000',
        'correct_answer': 2
    },
    {
        'question_text': 'Что означает IDE?',
        'option1': 'Integrated Development Environment',
        'option2': 'Internet Development Editor',
        'option3': 'Interactive Design Environment',
        'option4': 'International Data Exchange',
        'correct_answer': 1
    },
    {
        'question_text': 'Какая система контроля версий наиболее популярна?',
        'option1': 'SVN',
        'option2': 'Mercurial',
        'option3': 'Git',
        'option4': 'CVS',
        'correct_answer': 3
    },
    {
        'question_text': 'Что такое Docker?',
        'option1': 'Язык программирования',
        'option2': 'Платформа контейнеризации',
        'option3': 'База данных',
        'option4': 'Веб-сервер',
        'correct_answer': 2
    }
]

def add_questions():
    with app.app_context():
        added = 0
        
        for q_data in additional_questions:
            # Проверяем, не существует ли уже такой вопрос
            existing = Question.query.filter_by(question_text=q_data['question_text']).first()
            
            if not existing:
                question = Question(
                    question_text=q_data['question_text'],
                    option1=q_data['option1'],
                    option2=q_data['option2'],
                    option3=q_data['option3'],
                    option4=q_data['option4'],
                    correct_answer=q_data['correct_answer']
                )
                db.session.add(question)
                added += 1
        
        db.session.commit()
        
        total = Question.query.count()
        print(f"✓ Добавлено новых вопросов: {added}")
        print(f"✓ Всего вопросов в базе: {total}")

if __name__ == '__main__':
    print("Добавление дополнительных вопросов...")
    add_questions()
    print("Готово!")

