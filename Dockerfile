FROM python:3.12-slim
LABEL authors="Jerome"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install necessary dependencies for PostgreSQL
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libpq-dev \
       pkg-config \
       cron \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY ./cronjobs/fetch_steam_user_data /etc/cron.d/fetch_steam_user_data
RUN chmod 0644 /etc/cron.d/fetch_steam_user_data
RUN crontab /etc/cron.d/fetch_steam_user_data \
    && mkdir /var/log/cron

EXPOSE 8000

CMD ["sh", "-c", "cron && python manage.py runserver 0.0.0.0:8000"]
