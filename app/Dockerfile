# ==========================================
# Stage 1: Build & Install Dependencies
# ==========================================
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/workspace/.venv

WORKDIR /workspace

# 1. Copy pyproject.toml and uv.lock directly into /workspace
COPY pyproject.toml uv.lock ./

# 2. Sync dependencies using the cache (without installing our local code packages yet)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# 3. Copy the rest of the actual application files into the build context
COPY . .

# 4. Do the final sync to install our local project package fully into the virtual env
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# ==========================================
# Stage 2: Clean, Minimal Runtime Environment
# ==========================================
FROM python:3.12-slim-bookworm AS runner

WORKDIR /workspace

# Copy the environment and application from the builder stage
COPY --from=builder /workspace/.venv /workspace/.venv
COPY --from=builder /workspace/app /workspace/app

# Place virtualenv executables at the front of the PATH
ENV PATH="/workspace/.venv/bin:$PATH"

EXPOSE 8000

# Start your FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
