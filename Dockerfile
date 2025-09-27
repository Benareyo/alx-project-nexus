# Use an official Python runtime as base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Run Django server
CMD ["gunicorn", "project_nexus.wsgi:application", "--bind", "0.0.0.0:8000"]
