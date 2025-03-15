#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# command switches
case "$1" in
  admin)
    export DJANGO_SETTINGS_MODULE=e_comm_onion_arch.settings_admin
    exec su-exec $USER gunicorn e_comm_onion_arch.wsgi \
      -b 0.0.0.0:9000 \
      --log-level=$GUNICORN_LOG_LEVEL \
      2>&1
    ;;
  run)
    exec python manage.py runserver
  *)
    echo "Usage: $0 {admin}"
    exit 1
    ;;
esac
