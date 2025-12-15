FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --compile-bytecode --frozen --no-cache
ENV PATH="/app/.venv/bin:$PATH"

COPY main.py main.py
ENTRYPOINT python main.py
