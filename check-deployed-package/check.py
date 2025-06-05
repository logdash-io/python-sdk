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
logs_seed = os.environ.get('LOGS_SEED', 'default')
metrics_seed = os.environ.get('METRICS_SEED', '1')
print(f"Using API Key: {api_key}")
print(f"Using Logs Seed: {logs_seed}")
print(f"Using Metrics Seed: {metrics_seed}")

logdash = create_logdash({
    "api_key": api_key, 
})

# Get the logger instance
logger = logdash.logger

# Get the metrics instance
metrics = logdash.metrics

# Log some messages with seed appended
logger.log('This is an info log', logs_seed)
logger.error('This is an error log', logs_seed)
logger.warn('This is a warning log', logs_seed)
logger.debug('This is a debug log', logs_seed)
logger.http('This is a http log', logs_seed)  
logger.silly('This is a silly log', logs_seed)
logger.info('This is an info log', logs_seed)
logger.verbose('This is a verbose log', logs_seed)

# Set and mutate metrics with seed
metrics.set('users', metrics_seed)
metrics.mutate('users', 1)


# Wait to ensure data is sent
time.sleep(1) 