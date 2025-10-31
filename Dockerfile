# Dockerfile

# Start from a slim Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (e.g., for Pillow)
# You may need to add more if your libraries require them
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the container
COPY . /app/

# Set the default settings module
ENV DJANGO_SETTINGS_MODULE=personal_site.settings

# Run collectstatic as root
RUN python manage.py collectstatic --noinput



# Create a non-root user and group
RUN addgroup --system app && adduser --system --group app

# Create media directory and set permissions
RUN mkdir -p /app/media && chown -R app:app /app/media
RUN chown -R app:app /app/static

# --- ADD THIS LINE ---
# Give the app user ownership of the entire /app directory
RUN chown -R app:app /app/

# Switch to the non-root user
USER app

# This image will be used for both web and worker.
# The CMD will be provided by docker-compose.