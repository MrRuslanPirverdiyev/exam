"""
Скрипт для локального запуска приложения
Запустите командой: python run_local.py
"""

from app import app, init_db

if __name__ == '__main__':
    print("Инициализация базы данных...")
    init_db()
    print("База данных готова!")
    print("\n" + "="*50)
    print("Приложение запущено!")
    print("Откройте браузер по адресу: http://127.0.0.1:5000")
    print("Нажмите Ctrl+C для остановки сервера")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)

