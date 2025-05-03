# logdash - Python SDK

Logdash is a zero-config observability platform. This package serves as a Python interface to use it.

## Pre-requisites

Setup your free project in less than 2 minutes at [logdash.io](https://logdash.io/)

## Installation

```bash
pip install logdash
```

## Logging

```python
from logdash import create_logdash

# Initialize with your API key
logdash = create_logdash({
    # optional, but recommended to see your logs in the dashboard
    "api_key": "<your-api-key>",
})

# Access the logger
logger = logdash.logger

logger.info("Application started successfully")
logger.error("An unexpected error occurred")
logger.warn("Low disk space warning")
```

## Metrics

```python
from logdash import create_logdash

# Initialize with your API key
logdash = create_logdash({
    # optional, but recommended as metrics are only hosted remotely
    "api_key": "<your-api-key>",
})

# Access metrics
metrics = logdash.metrics

# to set absolute value
metrics.set("users", 0)

# to modify existing metric
metrics.mutate("users", 1)
```

## View

To see the logs or metrics, go to your project dashboard

![logs](docs/logs.png)
![delta](docs/delta.png)

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Support

If you encounter any issues, please open an issue on GitHub or let us know at [contact@logdash.io](mailto:contact@logdash.io).
