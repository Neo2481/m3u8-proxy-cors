# syntax=docker/dockerfile:1

# Use a lightweight Python base image
ARG PYTHON_VERSION=3.9.17
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing .pyc files & buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user to run the application
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Switch to the non-privileged user
USER appuser

# Copy the application source code
COPY . .

# Cloudflare expects the app to run on port 8080
EXPOSE 8080

# Run the application
CMD ["python", "main.py"]
