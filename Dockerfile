# Use a slim official Python base image
FROM python:3.11.8-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Copy requirements.txt first to benefit from Docker layer caching
COPY requirements.txt .

# Upgrade pip and install dependencies (no cache to keep image small)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc curl && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y build-essential gcc && apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /root/.cache

# Copy the rest of your application code
COPY . .

# Expose port
EXPOSE 80

# Start the Flask app via Gunicorn with config
CMD ["gunicorn", "--config", "gcorn_config.py", "app:app"]


## For local testing
# docker build -t image-generation-app .
# docker run -p 80:80 image-generation-app






