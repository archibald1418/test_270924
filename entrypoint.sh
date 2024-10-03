#!/usr/bin/env bash

alembic upgrade head

fastapi run main.py --port 8000 --workers 1
