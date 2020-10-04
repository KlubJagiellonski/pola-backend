release: python manage.py migrate && python manage.py collectstatic
web: gunicorn pola.config.wsgi:application
