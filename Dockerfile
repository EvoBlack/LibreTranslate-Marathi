FROM python:3.11.11-slim-bullseye

WORKDIR /app

# Avoid interactive prompts during apt installs
ARG DEBIAN_FRONTEND=noninteractive

# Install minimal system dependencies
RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        pkg-config \
        gcc \
        g++ \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Download MarianMT model for English-Marathi translation
RUN echo "Downloading MarianMT model..." \
    && python scripts/download_marianmt.py \
    && echo "Verifying model files..." \
    && ls -lh models/en-mr-marianmt/ \
    && test -f models/en-mr-marianmt/config.json || (echo "ERROR: Model not downloaded properly" && exit 1) \
    && echo "✓ Model downloaded successfully"

# Verify installation and model loading
RUN echo "Verifying installation..." \
    && python -c "import flask; print('✓ Flask:', flask.__version__)" \
    && python -c "import transformers; print('✓ Transformers:', transformers.__version__)" \
    && python -c "import torch; print('✓ PyTorch:', torch.__version__)" \
    && echo "✓ Core dependencies verified"

# Create non-root user
RUN addgroup --system --gid 1032 libretranslate \
    && adduser --system --uid 1032 --ingroup libretranslate libretranslate \
    && chown -R libretranslate:libretranslate /app

# Set environment variables
ENV PORT=5000 \
    LT_LOAD_ONLY=en,mr \
    LT_DISABLE_FILES_TRANSLATION=true \
    PYTHONUNBUFFERED=1 \
    TRANSFORMERS_OFFLINE=1 \
    PYTHONPATH=/app

# Make startup script executable
RUN chmod +x start.sh

# Switch to non-root user
USER libretranslate

# Expose port
EXPOSE ${PORT}

# Health check - give more time for startup
HEALTHCHECK --interval=30s --timeout=15s --start-period=90s --retries=3 \
    CMD python scripts/healthcheck.py || exit 1

# Start the application using the startup script
CMD ["./start.sh", "--host", "0.0.0.0", "--port", "5000", "--load-only", "en,mr", "--threads", "4", "--disable-files-translation"]
