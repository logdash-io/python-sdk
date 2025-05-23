#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import pkg_resources

print('=== LogDash SDK Demo ===')

from logdash import create_logdash

try:
    logdash_version = pkg_resources.get_distribution("logdash").version
except:
    logdash_version = "unknown"
print(f"Using logdash package version: {logdash_version}")
print()

api_key = os.environ.get('LOGDASH_API_KEY')
print(f"Using API Key: {api_key}")

logdash = create_logdash({
    "api_key": api_key, 
})

# Get the logger instance
logger = logdash.logger

# Get the metrics instance
metrics = logdash.metrics

# Log some messages
logger.log('This is an info log')
logger.error('This is an error log')

# Set and mutate metrics
metrics.set('demo_users', 42)
metrics.mutate('demo_counter', 1)

# Wait to ensure data is sent
time.sleep(1) 