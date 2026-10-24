import io
import subprocess
import sys
import textwrap
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from logdash import create_logdash


class TestFlush(unittest.TestCase):
    def test_flush_waits_for_logs_metrics_and_events(self):
        sent = []

        def slow_request(url, **kwargs):
            time.sleep(0.2)
            sent.append(url)

        with mock.patch("requests.post", side_effect=slow_request), mock.patch("requests.put", side_effect=slow_request), redirect_stdout(io.StringIO()):
            logdash = create_logdash({"api_key": "key", "host": "https://logdash.test"})
            logdash.logger.info("hello")
            logdash.metrics.set("users", 1)
            logdash.track("agent_run")
            logdash.flush()
            self.assertCountEqual(sent, ["https://logdash.test/logs", "https://logdash.test/metrics", "https://logdash.test/events"])

    def test_exit_waits_for_logs_metrics_and_events(self):
        script = textwrap.dedent("""
            import atexit
            import time
            from unittest import mock
            from logdash import create_logdash

            sent = []

            def slow_request(url, **kwargs):
                time.sleep(0.2)
                sent.append(url)

            # Exit handlers run after the interpreter has waited for the threads it waits for
            atexit.register(lambda: print("sent", sorted(sent)))
            mock.patch("requests.post", side_effect=slow_request).start()
            mock.patch("requests.put", side_effect=slow_request).start()
            logdash = create_logdash({"api_key": "key", "host": "https://logdash.test"})
            logdash.logger.info("hello")
            logdash.metrics.set("users", 1)
            logdash.track("agent_run")
        """)
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=str(Path(__file__).resolve().parent.parent),
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertIn(
            "sent ['https://logdash.test/events', 'https://logdash.test/logs', 'https://logdash.test/metrics']",
            result.stdout.splitlines(),
            result.stderr,
        )


if __name__ == "__main__":
    unittest.main()
