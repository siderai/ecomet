#!/bin/bash
set -e

source .env 2>/dev/null || true

CLICKHOUSE_URL="${CLICKHOUSE_URL:-http://localhost:8123}"
CLICKHOUSE_USER="${CLICKHOUSE_USER:-admin}"
CLICKHOUSE_PASSWORD="${CLICKHOUSE_PASSWORD:-password}"
CLICKHOUSE_DB="${CLICKHOUSE_DB:-test}"

until curl -s "${CLICKHOUSE_URL}/ping" > /dev/null; do
    echo "Waiting for ClickHouse..."
    sleep 2
done

echo "Creating database ${CLICKHOUSE_DB}..."
curl -s "${CLICKHOUSE_URL}/" \
    --user "${CLICKHOUSE_USER}:${CLICKHOUSE_PASSWORD}" \
    --data-binary "CREATE DATABASE IF NOT EXISTS ${CLICKHOUSE_DB}"

echo "Creating table from table.sql..."
head -n 7 table.sql | curl -s "${CLICKHOUSE_URL}/?database=${CLICKHOUSE_DB}" \
    --user "${CLICKHOUSE_USER}:${CLICKHOUSE_PASSWORD}" \
    --data-binary @-

echo "Loading data from table.sql..."
tail -n +9 table.sql | curl -s "${CLICKHOUSE_URL}/?database=${CLICKHOUSE_DB}" \
    --user "${CLICKHOUSE_USER}:${CLICKHOUSE_PASSWORD}" \
    --data-binary @-

echo "Database initialized successfully!"
