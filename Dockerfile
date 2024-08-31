# Dockerfile

# Use the official Python image from the Docker Hub
FROM python:3.12-slim-bookworm

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install OS package dependencies
RUN apt update; apt install -y --no-install-recommends --no-install-suggests python3-dev default-libmysqlclient-dev build-essential pkg-config

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . /app/
