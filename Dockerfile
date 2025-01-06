FROM python:3.12-slim
LABEL authors="Jerome"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install necessary dependencies
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
COPY ./cronjobs/daily_steam_update /etc/cron.d/daily_steam_update

# Set correct permissions for cron job files
RUN chmod 0644 /etc/cron.d/daily_steam_update

# Apply cron job files
RUN crontab /etc/cron.d/daily_steam_update

# reload cron service
RUN service cron reload

# Create log directory for cron
RUN mkdir -p /var/log/cron

# Expose the Django app port
EXPOSE 8000

# Run cron in the background and Django server in the foreground
CMD ["sh", "-c", "cron -f & python manage.py runserver 0.0.0.0:8000"]
