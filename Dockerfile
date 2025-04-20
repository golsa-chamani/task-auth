FROM python:3.9-slim-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m django
USER django
WORKDIR /home/django/app

COPY --chown=django requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

COPY --chown=django . .

ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --no-cache-dir gunicorn

CMD ["/home/django/.local/bin/gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]