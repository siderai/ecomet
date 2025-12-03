#!/bin/bash
set -e

source .env 2>/dev/null || true

CLICKHOUSE_URL="${CLICKHOUSE_URL:-http://localhost:8123}"
CLICKHOUSE_USER="${CLICKHOUSE_USER:-admin}"
CLICKHOUSE_PASSWORD="${CLICKHOUSE_PASSWORD:-password}"
CLICKHOUSE_DB="${CLICKHOUSE_DB:-test}"

echo "Executing query..."
echo ""

curl -s "${CLICKHOUSE_URL}/?database=${CLICKHOUSE_DB}" \
    --user "${CLICKHOUSE_USER}:${CLICKHOUSE_PASSWORD}" \
    --data-binary @query.sql \
    -H "Content-Type: text/plain" | \
    awk -F'\t' '{printf "%-20s | %s\n", $1, $2}'
