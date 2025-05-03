#!/usr/bin/env python3
"""
Basic usage example for the logdash SDK.
"""

import time
from logdash import create_logdash


def main():
    """Main function demonstrating logdash usage."""
    # Initialize logdash with your API key
    # For testing without an API key, logs will only be printed locally
    logdash = create_logdash({
        "api_key": "your-api-key",  # Replace with your actual API key
        "host": "https://api.logdash.io",
        "verbose": True,  # Enable verbose mode for development
    })

    # Get the logger instance
    logger = logdash.logger
    
    # Get the metrics instance
    metrics = logdash.metrics
    
    # Log messages at different levels
    logger.info("Application started")
    logger.debug("Debug information")
    logger.warn("Warning message")
    logger.error("Error occurred")
    logger.http("HTTP request processed")
    logger.verbose("Verbose details")
    
    # Track metrics
    for i in range(5):
        # Set absolute values
        metrics.set("active_users", 100 + i * 10)
        
        # Mutate values (increment/decrement)
        metrics.mutate("requests_count", 1)
        
        logger.info(f"Iteration {i+1}/5 completed")
        time.sleep(1)
        
    logger.info("Example completed")


if __name__ == "__main__":
    main() 