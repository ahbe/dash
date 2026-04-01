#!/bin/bash
# domino_job.sh

echo "Starting Domino job..."

# Ensure uv is in PATH
export PATH="/usr/local/bin:$PATH"

# Activate uv environment
if [ -d ".venv" ]; then
  echo "Activating existing virtual environment."
  source ./.venv/bin/activate
elif uv venv; then
  echo "Created new virtual environment."
  source ./.venv/bin/activate
else
  echo "Error: Failed to create or activate uv virtual environment."
  exit 1
fi

# Install dependencies (if not already synced)
uv sync

# Ensure .env is present (Domino often uses project env vars directly)
if [ ! -f ".env" ]; then
  echo "WARNING: .env file not found. Assuming environment variables are set directly in Domino."
  cp .env.example .env # Create a dummy .env if none exists
fi

# Run the Dash app
echo "Running Dash application in production mode..."
uv run python run_server.py

echo "Domino job finished."
