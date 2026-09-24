#!/bin/sh
# Inicia a aplicação em produção: aplica as migrações, cria o administrador
# (se DJANGO_SUPERUSER_* estiverem definidas) e sobe o Gunicorn.
set -e

python manage.py migrate --noinput
python manage.py ensure_superuser
exec gunicorn config.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers "${WEB_CONCURRENCY:-2}" \
    --access-logfile -
