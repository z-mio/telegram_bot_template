FROM python:3.12-slim AS build

COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project --frozen

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

FROM python:3.12-slim AS runtime

WORKDIR /app
COPY --from=build /app /app

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "bot.py"]