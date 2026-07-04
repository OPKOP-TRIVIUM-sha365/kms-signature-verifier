FROM python:3.11-slim

LABEL maintainer="Vildan KULJANOVIĆ <kuljanovic99@icloud.com>"
LABEL description="KMS Signature Verifier - Professional toolkit for offline KMS signature verification"
LABEL version="1.0"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 \
    openssl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY verify_kms_signature.py .
COPY convert_public_key.py .
COPY sign_and_verify_msg.py .
COPY sign_and_verify_msg.sh .

# Make scripts executable
RUN chmod +x verify_kms_signature.py && \
    chmod +x convert_public_key.py && \
    chmod +x sign_and_verify_msg.py && \
    chmod +x sign_and_verify_msg.sh

# Create non-root user for security
RUN useradd -m -u 1000 verifier && \
    mkdir -p /home/verifier/.gnupg && \
    chmod 700 /home/verifier/.gnupg

# Set working directory for user
WORKDIR /work

# Switch to non-root user
USER verifier

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)"

# Default entrypoint
ENTRYPOINT ["python3", "/app/verify_kms_signature.py"]
CMD ["--help"]
