# Base image
FROM python:3.12

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port Django runs on
EXPOSE 8000

# Run Django application
CMD ["sh", "-c", "export $(cat .env | xargs) && gunicorn --bind 0.0.0.0:8000 TraumaCare.wsgi:application"]