#!/bin/sh
set -e

echo "Building LogDash demo Docker image (using published package)..."
docker build --no-cache -t logdash-python-demo -f check-deployed-package/Dockerfile .

echo
echo "Running LogDash demo..."
echo

# Run in non-interactive mode which works everywhere
docker run --rm \
  -e LOGDASH_API_KEY="${LOGDASH_API_KEY}" \
  logdash-python-demo

echo
echo "Demo completed!" 