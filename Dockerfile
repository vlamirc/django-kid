# syntax=docker/dockerfile:1

# ---------------------------------------------------------------------------
# base: Python + uv + dependências de produção
# ---------------------------------------------------------------------------
FROM python:3.13-slim-bookworm AS base

COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# ---------------------------------------------------------------------------
# dev: usado pelo docker compose. O código entra por volume, com recarga automática.
# ---------------------------------------------------------------------------
FROM base AS dev

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ---------------------------------------------------------------------------
# prod: imagem final (último estágio, é o que as plataformas de nuvem usam).
# ---------------------------------------------------------------------------
FROM base AS prod

COPY . .

# collectstatic não acessa o banco; as variáveis abaixo existem só para o build.
RUN SECRET_KEY=build DATABASE_URL=postgres://build@localhost/build \
    python manage.py collectstatic --noinput

RUN useradd --create-home --uid 1000 app && chown -R app /app
USER app

EXPOSE 8000
CMD ["./scripts/start-prod.sh"]
