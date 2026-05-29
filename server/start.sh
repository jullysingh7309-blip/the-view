#!/bin/bash
set -e
cd "$(dirname "$0")/src" 2>/dev/null || cd src
exec gunicorn --bind "0.0.0.0:${PORT:-8080}" --workers 1 --threads 8 --timeout 120 app:app
