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

# Copy cron job files
COPY ./cronjobs/fetch_steam_user_data /etc/cron.d/fetch_steam_user_data
COPY ./cronjobs/fetch_steam_games_data /etc/cron.d/fetch_steam_games_data

# Set correct permissions for the cron job files
RUN chmod 0644 /etc/cron.d/fetch_steam_user_data /etc/cron.d/fetch_steam_games_data

# Add the cron jobs to the crontab and create the log directory
RUN crontab /etc/cron.d/fetch_steam_user_data \
    && crontab /etc/cron.d/fetch_steam_games_data \
    && mkdir -p /var/log/cron


EXPOSE 8000

CMD ["sh", "-c", "cron && python manage.py runserver 0.0.0.0:8000"]
