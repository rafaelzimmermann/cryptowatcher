#!/bin/sh

set -x

echo "Waiting for postgres..."

while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

exec "$@"
