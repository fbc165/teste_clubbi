#!/bin/sh
echo "==== Applying database migrations ===="
alembic -c /api/storage/postgresql/alembic.ini upgrade head

echo "\n==== Running application ===="
uvicorn api.app:app --host 0.0.0.0 --port 9900