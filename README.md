# Music Project

Система з підбору музики.

Overview
=====
Перш ніж розпочати, переконайтеся, що у вас встановлено Python та pip. Потім виконайте наступні кроки:

1. Клонуйте репозиторій:

```bash
git clone https://github.com/username/music_django.git
```

2. Перейдіть у папку проекту:

```bash
cd music_django
```

3. Встановіть віртуальне середовище:

```bash
python -m venv venv
```

4. Активуйте віртуальне середовище(для Linux/Mac):

```bash
source venv/bin/activate
```
Активуйте віртуальне середовище(для Windows):

```bash
venv\Scripts\activate
```

5. Встановіть залежності:

```bash
pip install -r requirements.txt
```

6. Зробіть міграції:

```bash
python manage.py migrate
```

7. Запустіть сервер:

```bash
python manage.py runserver
```

8. Створіть суперкористувача:

```bash
python manage.py createsuperuser
```
Введіть ім'я користувача, електронну пошту та пароль.

9. Перейдіть за посиланням [http://localhost:8000/](http://localhost:8000/)




