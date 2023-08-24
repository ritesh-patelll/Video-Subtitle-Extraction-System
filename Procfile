web: gunicorn humblebee.wsgi:application
worker: celery -A humblebee worker -l info -P eventlet