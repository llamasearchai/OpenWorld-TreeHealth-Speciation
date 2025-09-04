FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml hatch.toml README.md LICENSE datasette.yml ./
COPY openworld_tshm ./openworld_tshm
COPY scripts ./scripts

RUN python -m pip install --upgrade pip && \
    python -m pip wheel --no-cache-dir --wheel-dir /wheels ".[llm]"

FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd -m appuser
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN python -m pip install --no-cache-dir /wheels/*
COPY pyproject.toml hatch.toml README.md LICENSE datasette.yml ./
COPY openworld_tshm ./openworld_tshm
COPY scripts ./scripts

USER appuser
EXPOSE 8000

# Create a simple health check script
RUN echo '#!/bin/bash\n\
python -c "import httpx; r = httpx.get('\''http://127.0.0.1:8000/api/health'\'', timeout=2); exit(0 if r.status_code==200 and r.json().get('\''status'\'')=='\''ok'\'' else 1)"' > /app/healthcheck.sh && \
chmod +x /app/healthcheck.sh

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s CMD /app/healthcheck.sh

CMD ["openworld-tshm", "dashboard", "--host", "0.0.0.0", "--port", "8000"]

