# ── Stage 1: builder ─────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

# Install build dependencies (needed for faster-whisper, sentencepiece, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy requirements first to leverage layer caching
COPY requirements.txt .

# Install all Python dependencies into a prefix we can copy later
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: runtime ─────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Copy only the installed packages from the builder stage
COPY --from=builder /install /usr/local

WORKDIR /app

# Copy application source
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Create the meetings directory so the volume mount has a sensible default
RUN mkdir -p /app/meetings

# Expose FastAPI port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
