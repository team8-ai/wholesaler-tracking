# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables for non-interactive installs
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/opt/render/.cache/ms-playwright

# Install system dependencies required by Playwright's browsers
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # General Playwright dependencies (from Playwright docs, might overlap or be more comprehensive)
    libnss3 \
    libnspr4 \
    libdbus-glib-1-2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libasound2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxrender1 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libpango-1.0-0 \
    libharfbuzz0b \
    libfontconfig1 \
    libfreetype6 \
    # Clean up
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

# Copy the application code
COPY src/ /app/src/

# Entry point
CMD ["python", "src/main.py"] 