FROM python:3.11-slim

WORKDIR /app

# Install minimal system dependencies
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements-simple.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY scripts/ scripts/

# Download model
RUN python scripts/download_marianmt.py && \
    test -f models/en-mr-marianmt/config.json || exit 1

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Environment variables
ENV PORT=5000 \
    HOST=0.0.0.0 \
    PYTHONUNBUFFERED=1

EXPOSE ${PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Start application
CMD ["python", "app.py"]
