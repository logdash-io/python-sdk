import re
import uuid
from typing import Any, Dict, Optional, Union

import requests

from logdash.internal import internal_logger

EVENT_NAME = re.compile(r"[a-z][a-z0-9_]{0,63}")
WEBSITE_EVENTS = ("pageview", "pageleave", "browser_error")

EventProps = Dict[str, Union[str, int, float, bool]]
UserId = Union[str, int]


class Events:
    def __init__(self, api_key: str, host: str, verbose: bool = False, app: Optional[str] = None):
        self.api_key = api_key
        self.host = host
        self.verbose = verbose
        self.app = app

    def create(self, name: str, props: Optional[EventProps] = None, user_id: Optional[UserId] = None) -> Optional[Dict[str, Any]]:
        """Build the event body, or warn and return None when the server would reject the event."""
        if not isinstance(name, str) or not EVENT_NAME.fullmatch(name) or name in WEBSITE_EVENTS:
            internal_logger.warn(
                f"Dropping event {name!r}: its name must match [a-z][a-z0-9_]{{0,63}} "
                "and not be pageview, pageleave or browser_error"
            )
            return None
        if user_id is not None and "@" in str(user_id):
            internal_logger.warn(f"Dropping event {name!r}: user_id must be an internal ID, never an email address")
            return None

        if self.verbose:
            internal_logger.verbose(f"Tracking event {name}")

        return {
            # The server stores an event once per id, so a retry must send the same one
            "id": str(uuid.uuid4()),
            "name": name,
            # A copy, so the caller can change its dict while the event is being sent
            **({"props": dict(props)} if props else {}),
            **({"userId": user_id} if user_id is not None else {}),
            **({"app": self.app} if self.app else {}),
        }

    def send(self, event: Dict[str, Any]) -> None:
        try:
            requests.post(
                f"{self.host}/events",
                headers={
                    "Content-Type": "application/json",
                    "project-api-key": self.api_key,
                },
                json=event,
                timeout=5,  # Add timeout to prevent blocking
            )
        except requests.RequestException:
            # Silently fail like logs and metrics
            pass
