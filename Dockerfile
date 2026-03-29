# Use an official Python runtime
FROM python:3.10-slim

# Set environment variables so Python behaves well in Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (required for Postgres and other packages)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy your entire Django project into the /app folder
COPY . /app/

# Create the folder where Railway will mount your Persistent Volume
RUN mkdir -p /app/media

# Collect static files for WhiteNoise
RUN python manage.py collectstatic --noinput

# Run database migrations and start Gunicorn
CMD python manage.py migrate && gunicorn personal_site.wsgi:application --bind 0.0.0.0:$PORT