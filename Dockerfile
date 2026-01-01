# Build stage for installing dependencies and browsers
# Use a small Python 3.12 base image as the build stage
FROM python:3.12-slim as builder

# Set work directory inside the image
WORKDIR /app

# Copy requirements.txt to the working directory (needed for installing dependencies)
COPY requirements.txt .

# Upgrade pip, install Python dependencies from requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install system packages and browsers required for Playwright tests
# Keep the list minimal and use --no-install-recommends to reduce image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        wget \
        fonts-liberation \
        libnss3 \
        libxss1 \
        libasound2 \
        libatk1.0-0 \
        libatk-bridge2.0-0 \
        libcups2 \
        libdrm2 \
        libxrandr2 \
        libgbm1 \
        libxcomposite1 \
        libxdamage1 \
        libxfixes3 \
        libx11-xcb1 \
        libgtk-3-0 \
        curl \
        unzip \
        xvfb \
        libpangocairo-1.0-0 \
        libxshmfence1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Playwright default's browsers: (Chromium, Firefox, Webkit) and optional browsers: (Chrome, Edge)
RUN playwright install chrome msedge --with-deps

# Final stage - reuse the builder image (keeps layers and installed packages)
FROM builder

# PYTHONUNBUFFERED ensures logs are flushed immediately
ENV PYTHONUNBUFFERED=1

# Ensure same working directory in the final image
WORKDIR /app

# Copy project files: Copy everything from the current directory on your host (the build context) into the current working directory inside the container.
COPY . .

# Create writable directories for reports and logs that are also mounted from host
RUN mkdir -p reports logs && \
    chmod 777 reports logs
