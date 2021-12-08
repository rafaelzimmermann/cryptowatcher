#!/bin/sh

set -x

echo "Waiting for postgres..."

while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 10
done

echo "PostgreSQL started"

exec "$@"
