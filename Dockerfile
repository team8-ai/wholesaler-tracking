# Stage 1: Build stage with Playwright dependencies
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy AS build

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY src/ /app/src/

# Stage 2: Final stage
FROM python:3.11-slim-jammy

# Set working directory
WORKDIR /app

# Create a non-root user
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Copy installed dependencies from the build stage
COPY --from=build /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=build /root/.cache/ms-playwright/ /home/appuser/.cache/ms-playwright/

# Copy the application code
COPY --chown=appuser:appuser src/ /app/src/

# Set environment variables for playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/home/appuser/.cache/ms-playwright

# Entry point
CMD ["python", "src/main.py"] 