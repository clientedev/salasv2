#!/bin/bash
uv run gunicorn --bind 0.0.0.0:${PORT:-5000} --reuse-port main:app
