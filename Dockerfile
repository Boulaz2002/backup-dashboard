# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install tzdata and system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
