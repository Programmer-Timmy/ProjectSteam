FROM python:3.12-slim
LABEL authors="Jerome"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Set the time zone to Europe/Amsterdam
RUN ln -fs /usr/share/zoneinfo/Europe/Amsterdam /etc/localtime
RUN echo "Europe/Amsterdam" > /etc/timezone

# Set the environment variable for TZ
ENV TZ=Europe/Amsterdam

# Install necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
      procps \
      gcc \
      libpq-dev \
      pkg-config \
      dos2unix \
      cron \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy cron job files
COPY ./cronjobs/daily_steam_update /etc/cron.d/daily_steam_update

# Set correct permissions for cron job files
RUN chmod 0644 /etc/cron.d/daily_steam_update

RUN dos2unix /etc/cron.d/daily_steam_update

RUN crontab /etc/cron.d/daily_steam_update

RUN touch /var/log/cron.log

EXPOSE 8000

# Run cron in the background and Django server in the foreground
CMD ["sh", "-c", "cron && manage.py makemigrations & python manage.py migrate & python manage.py runserver 0.0.0.0:8000"]
