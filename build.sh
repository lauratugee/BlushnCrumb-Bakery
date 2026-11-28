#!/usr/bin/env bash
set -o errexit

python -m pip install -e .
python manage.py collectstatic --noinput
python manage.py migrate --noinput
