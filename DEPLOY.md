# Deployment Guide — Meeting Intelligence System

> [!NOTE]
> This guide covers three deployment modes: local Python dev, Docker dev (LiveKit only), and full Docker production (backend + LiveKit + Ollama).

---

## Table of Contents
1. [Local Dev](#1-local-dev)
2. [Docker Dev](#2-docker-dev-livekit-only)
3. [Docker Production](#3-docker-production-full-stack)
4. [Environment Variables](#4-environment-variables)
5. [Scaling — Nginx Reverse Proxy](#5-scaling--nginx-reverse-proxy)
6. [Health Checks](#6-health-checks)

---

## 1. Local Dev

Run everything directly on your machine (fastest iteration loop).

```bash
# 1. Clone and enter the project
git clone <repo-url>
cd Cross-platfrom-ai-meeting-summarizer

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and edit environment variables
cp .env.example .env
# Edit .env — set WHISPER_MODEL, OLLAMA_MODEL, LiveKit keys, etc.

# 5. Start LiveKit (requires Docker)
docker compose up -d

# 6. Start Ollama (separate terminal, or use the Docker service below)
ollama serve
ollama pull llama3.1:8b

# 7. Start the FastAPI backend
uvicorn backend.main:app --reload --port 8000

# 8. Open the app
# http://localhost:8000/app/index.html
```

---

## 2. Docker Dev (LiveKit only)

Use when you want LiveKit containerised but run the Python backend natively (e.g. for hot-reload).

```bash
# Start only the LiveKit container
docker compose up -d

# Then run the backend as in step 7 above
uvicorn backend.main:app --reload --port 8000
```

---

## 3. Docker Production (full stack)

One-command deployment of **backend + LiveKit + Ollama**.

```bash
# 1. Build and start all services
docker compose -f docker-compose.prod.yml up -d --build

# 2. Pull Ollama model (first time only)
docker exec -it ollama ollama pull llama3.1:8b

# 3. Open the app
# http://localhost:8000/app/index.html
```

> [!IMPORTANT]
> Before deploying to a public server, update `livekit.yaml`:
> - Set `use_external_ip: true`
> - Replace the development keys (`devkey` / `devsecret_at_least_32_chars_long!`) with strong random secrets.
> - Mirror those secrets in your `.env` file.

To stop the stack:

```bash
docker compose -f docker-compose.prod.yml down
```

To stop **and** remove all data volumes (⚠ deletes stored Ollama models):

```bash
docker compose -f docker-compose.prod.yml down -v
```

---

## 4. Environment Variables

Copy `.env.example` to `.env` and customise before first run.

| Variable | Default | Description |
|---|---|---|
| `WHISPER_MODEL` | `small` | Whisper model size: `tiny`, `base`, `small`, `medium`, `large-v3` |
| `WHISPER_DEVICE` | `cpu` | `cpu` or `cuda` (GPU) |
| `WHISPER_COMPUTE` | `int8` | Quantisation: `int8` (CPU), `float16` (GPU) |
| `OLLAMA_MODEL` | `llama3.1:8b` | Ollama model tag to use for summarisation |
| `NLLB_MODEL` | `facebook/nllb-200-distilled-600M` | HuggingFace translation model |
| `LIVEKIT_URL` | `ws://localhost:7880` | LiveKit server WebSocket URL |
| `LIVEKIT_API_KEY` | `devkey` | LiveKit API key (change in production!) |
| `LIVEKIT_API_SECRET` | `devsecret_at_least_32_chars_long!` | LiveKit API secret (change in production!) |
| `MEETINGS_DIR` | `meetings` | Directory for meeting records and audio clips |

> [!CAUTION]
> Never commit a `.env` file containing real secrets to version control. The `.gitignore` excludes it, but double-check before pushing.

---

## 5. Scaling — Nginx Reverse Proxy

Run the stack behind Nginx so you can serve on standard ports (80/443) and add TLS.

**`nginx.conf` snippet:**

```nginx
upstream backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    # Redirect all HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate     /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # FastAPI app + WebSocket upgrade
    location / {
        proxy_pass         http://backend;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade $http_upgrade;
        proxy_set_header   Connection "upgrade";
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;   # keep WebSocket connections alive
    }
}
```

> [!TIP]
> Use [Certbot](https://certbot.eff.org/) to obtain a free Let's Encrypt TLS certificate automatically.

---

## 6. Health Checks

Verify each service after `docker compose -f docker-compose.prod.yml up -d`.

### Backend (FastAPI)

```bash
curl http://localhost:8000/health
# Expected: {"status":"ok"}  (or HTTP 200 root redirect)
```

### LiveKit

```bash
curl http://localhost:7880
# Expected: HTTP 200 with LiveKit version info
```

### Ollama

```bash
curl http://localhost:11434
# Expected: "Ollama is running"
```

### Docker service status

```bash
docker compose -f docker-compose.prod.yml ps
# All services should show "running (healthy)" or "running"
```

### Logs

```bash
# Tail all services
docker compose -f docker-compose.prod.yml logs -f

# Single service
docker compose -f docker-compose.prod.yml logs -f backend
docker compose -f docker-compose.prod.yml logs -f ollama
docker compose -f docker-compose.prod.yml logs -f livekit
```
