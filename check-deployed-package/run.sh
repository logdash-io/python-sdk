#!/bin/sh
set -e

# Generate random 5-character seed
LOGS_SEED=$(openssl rand -hex 2 | cut -c1-5)
echo "Generated seed: $LOGS_SEED"

# Generate random metrics seed (1-1,000,000)
METRICS_SEED=$(awk 'BEGIN{srand(); print int(rand()*1000000)+1}')
echo "Generated metrics seed: $METRICS_SEED"

echo "Building LogDash demo Docker image (using published package)..."
docker build --no-cache -t logdash-python-demo -f check-deployed-package/Dockerfile .

echo
echo "Running LogDash demo..."
echo

# Run in non-interactive mode which works everywhere
docker run --rm \
  -e LOGDASH_API_KEY="${LOGDASH_API_KEY}" \
  -e LOGS_SEED="${LOGS_SEED}" \
  -e METRICS_SEED="${METRICS_SEED}" \
  logdash-python-demo

echo
echo "Demo completed!" 

echo
echo "Authenticating with LogDash API..."

# Authenticate with API using the API key
AUTH_RESPONSE=$(curl -s -X 'POST' \
  'https://api.logdash.io/auth/api-key' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d "{
  \"apiKey\": \"${LOGDASH_API_KEY}\"
}")

# Extract token and projectId from response
TOKEN=$(echo "$AUTH_RESPONSE" | grep -o '"token":"[^"]*"' | sed 's/"token":"\(.*\)"/\1/')
PROJECT_ID=$(echo "$AUTH_RESPONSE" | grep -o '"projectId":"[^"]*"' | sed 's/"projectId":"\(.*\)"/\1/')

if [ -z "$TOKEN" ] || [ -z "$PROJECT_ID" ]; then
    echo "Error: Failed to authenticate with LogDash API"
    echo "Response: $AUTH_RESPONSE"
    exit 1
fi

echo "Authentication successful. Project ID: $PROJECT_ID"

echo
echo "Fetching logs from LogDash API..."

# Fetch logs from the API
LOGS_RESPONSE=$(curl -s -X 'GET' \
  "https://api.logdash.io/projects/${PROJECT_ID}/logs?limit=10" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer ${TOKEN}")

echo "Logs fetched successfully"

echo
echo "Validating log messages..."

# Expected log messages with seed
EXPECTED_MESSAGES="This is an info log ${LOGS_SEED}
This is an error log ${LOGS_SEED}
This is a warning log ${LOGS_SEED}
This is a debug log ${LOGS_SEED}
This is a http log ${LOGS_SEED}
This is a silly log ${LOGS_SEED}
This is an info log ${LOGS_SEED}
This is a verbose log ${LOGS_SEED}"

# Check if all expected messages are present in the logs
echo "$EXPECTED_MESSAGES" | while IFS= read -r expected_msg; do
    if ! echo "$LOGS_RESPONSE" | grep -q "$expected_msg"; then
        echo "Error: Expected log message not found: '$expected_msg'"
        echo "Logs response: $LOGS_RESPONSE"
        exit 1
    fi
    echo "✓ Found: '$expected_msg'"
done

echo
echo "Fetching metrics from LogDash API..."

# Fetch metrics from the API
METRICS_RESPONSE=$(curl -s -X 'GET' \
  "https://api.logdash.io/projects/${PROJECT_ID}/metrics" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer ${TOKEN}")

echo "Metrics fetched successfully"

echo
echo "Validating metrics..."

# Expected users metric value (metrics_seed + 1)
EXPECTED_USERS_VALUE=$((METRICS_SEED + 1))

# Check if users metric exists with correct value
if ! echo "$METRICS_RESPONSE" | grep -q '"name":"users"'; then
    echo "Error: Users metric not found"
    echo "Metrics response: $METRICS_RESPONSE"
    exit 1
fi

# Extract the value of the users metric and check if it matches expected value
USERS_VALUE=$(echo "$METRICS_RESPONSE" | sed 's/},{/}\n{/g' | grep '"name":"users"' | grep -o '"value":[0-9]*' | sed 's/"value"://')

if [ "$USERS_VALUE" != "$EXPECTED_USERS_VALUE" ]; then
    echo "Error: Users metric value mismatch. Expected: $EXPECTED_USERS_VALUE, Found: $USERS_VALUE"
    echo "Metrics response: $METRICS_RESPONSE"
    exit 1
fi

echo "✓ Found users metric with correct value: $USERS_VALUE"

echo
echo "All expected log messages and metrics found successfully!"
echo "Validation completed!"