# Use an official Python runtime as the base image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    build-essential

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies from requirements.txt
RUN pip install -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Run gunicorn to serve the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]