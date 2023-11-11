# Первая мультиагентная система

Проект тестировался с третьей версией Python.

Рекомендуется настроить виртуальное окружение. Вот "правильные" ссылки:
[https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html) и 
[https://virtualenv.pypa.io/en/stable/userguide/](https://docs.python.org/3/library/venv.html)
На Windows-машине это можно сделать из командной строки:

```
python -m venv env
call env/scripts/activate.bat
```

После этого надо установить необходимые модули

```
pip install -r requirements.txt
```
Структура проекта
1. main.py - точка входа. Читает информацию о заказах и курьерах из файла, создает агентов.
2. entities - содержит реализацию классов предметной области
3. agents - реализация классов для работы агентов.
4. utils - служебные классы