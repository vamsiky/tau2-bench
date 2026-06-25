#!/usr/bin/env bash
# Launch the LiteLLM proxy for this repo (subscription pass-through for Claude Code).
#
#   ./scripts/start-litellm.sh
#
# IMPORTANT: this proxy must run WITHOUT ANTHROPIC_API_KEY in its environment.
# The pass-through route has no api_key so that LiteLLM forwards Claude Code's
# subscription OAuth upstream; if ANTHROPIC_API_KEY were present, that route
# would inject it and override the subscription token. So we do NOT load .env
# here, and we defensively unset the key.
#
# tau2-bench uses the API key separately — it reads ANTHROPIC_API_KEY from .env
# via python-dotenv and talks to Anthropic directly, not through this proxy.
set -euo pipefail
cd "$(dirname "$0")/.."

# shellcheck disable=SC1091
source .venv/bin/activate

unset ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN

export LITELLM_MASTER_KEY="${LITELLM_MASTER_KEY:-sk-litellm-master-key}"
export DATABASE_URL="${DATABASE_URL:-postgresql://litellm:litellm@localhost:5433/litellm}"

# Postgres lives in podman container `litellm-db`; start it if it's stopped.
if command -v podman >/dev/null 2>&1; then
  podman start litellm-db >/dev/null 2>&1 || true
fi

exec litellm --config litellm_config.yaml --port 4000
