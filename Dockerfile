# Use the official Python image from the Docker Hub
FROM python:3.12-alpine

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install OS package dependencies
RUN apk add --no-cache mariadb-dev

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN apk add --no-cache --virtual build-deps gcc python3-dev musl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del build-deps gcc python3-dev musl-dev 

# Copy the entire Django project into the container
COPY . /app/
