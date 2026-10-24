# LogDash Python SDK Demo

Use command below to test if the published SDK works:

```
LOGDASH_API_KEY=<your-api-key> LOGDASH_PERSONAL_API_KEY=<your-personal-api-key> ./check-deployed-package/run.sh
```

`LOGDASH_API_KEY` sends the logs and metrics: the ingest key of the shared "SDK smoke tests" domain, from its Settings page.
They arrive as the `python-sdk` app on that domain.
`LOGDASH_PERSONAL_API_KEY` reads them back: a personal API key (`ldp_`) with logs:read and metrics:read, restricted to that domain.
It checks the latest version on PyPI; set `LOGDASH_VERSION` to check another one.
