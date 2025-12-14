FROM python:3.11-slim

WORKDIR /app

# Install minimal system dependencies
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY translations_dict.json .
COPY scripts/ scripts/

# Download IndicTrans2 model
RUN python scripts/download_indictrans2.py && \
    test -f models/indictrans2-en-mr/config.json || exit 1

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Environment variables
ENV PORT=7860 \
    HOST=0.0.0.0 \
    PYTHONUNBUFFERED=1

EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Start application
CMD ["python", "app.py"]
