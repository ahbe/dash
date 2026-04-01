# Stage 1: Build dependencies
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# Install uv
RUN apt-get update && apt-get install -y curl build-essential
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Copy pyproject.toml and uv.lock (if exists for caching)
COPY pricing-derogation-dashboard/pyproject.toml ./pyproject.toml
# COPY uv.lock ./uv.lock # Uncomment if you want to use a pre-generated uv.lock

# Sync dependencies to a virtual environment
RUN uv venv && uv sync

# Stage 2: Runtime image
FROM python:3.11-slim-bookworm

WORKDIR /app

# Copy uv-managed virtual environment from builder stage
COPY --from=builder /app/.venv ./.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY pricing-derogation-dashboard/src ./src
COPY pricing-derogation-dashboard/run_server.py ./run_server.py
COPY pricing-derogation-dashboard/data ./data
COPY pricing-derogation-dashboard/pyproject.toml ./pyproject.toml
COPY pricing-derogation-dashboard/.env.example ./.env.example
COPY pricing-derogation-dashboard/scripts ./scripts

# Create .env file from example for Docker environment
RUN cp .env.example .env

# Expose the port Dash runs on
EXPOSE 8050

# Run the Dash app with Gunicorn
CMD ["uv", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:8050", "run_server:server"]
