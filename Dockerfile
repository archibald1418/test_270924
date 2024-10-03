FROM python:3.11-slim-bookworm

WORKDIR /app
COPY requirements.txt alembic.ini ./
COPY scripts ./scripts
RUN pip install --no-cache-dir -r requirements.txt
COPY src .
COPY --chmod=0755 entrypoint.sh .

ENTRYPOINT /app/entrypoint.sh
