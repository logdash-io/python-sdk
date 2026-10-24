import io
import subprocess
import sys
import textwrap
import time
import unittest
import uuid
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from logdash import create_logdash


class TestEvents(unittest.TestCase):
    def track(self, params, *args, **kwargs):
        with mock.patch("requests.post") as post:
            logdash = create_logdash(params)
            logdash.track(*args, **kwargs)
            logdash.flush()
        return post.call_args_list

    def test_posts_the_event(self):
        [call] = self.track({"api_key": "key", "host": "https://logdash.test"}, "agent_run", {"model": "opus", "tools": 3, "cached": True})
        self.assertEqual(call.args, ("https://logdash.test/events",))
        self.assertEqual(call.kwargs["headers"], {"Content-Type": "application/json", "project-api-key": "key"})
        event = call.kwargs["json"]
        self.assertEqual(uuid.UUID(event.pop("id")).version, 4)
        self.assertEqual(event, {"name": "agent_run", "props": {"model": "opus", "tools": 3, "cached": True}})

    def test_events_get_their_own_id(self):
        with mock.patch("requests.post") as post:
            logdash = create_logdash({"api_key": "key"})
            logdash.track("agent_run")
            logdash.track("agent_run")
            logdash.flush()
        first, second = (call.kwargs["json"]["id"] for call in post.call_args_list)
        self.assertNotEqual(first, second)

    def test_events_carry_app(self):
        [call] = self.track({"api_key": "key", "app": "desktop"}, "agent_run")
        self.assertEqual(call.kwargs["json"]["app"], "desktop")

    def test_events_leave_out_app_when_unset(self):
        for params in ({}, {"app": None}, {"app": ""}):
            with self.subTest(params=params):
                [call] = self.track({"api_key": "key", **params}, "agent_run")
                self.assertNotIn("app", call.kwargs["json"])

    def test_events_carry_user_id(self):
        for user_id in ("42", 42, 0):
            with self.subTest(user_id=user_id):
                [call] = self.track({"api_key": "key"}, "agent_run", user_id=user_id)
                self.assertEqual(call.kwargs["json"]["userId"], user_id)

    def test_invalid_events_are_dropped_with_a_warning(self):
        for name, user_id in (
            ("Agent run", None),
            ("", None),
            ("9lives", None),
            ("a" * 65, None),
            ("agent_run\n", None),
            ("pageview", None),
            (None, None),
            ("agent_run", "alice@example.com"),
        ):
            with self.subTest(name=name, user_id=user_id):
                output = io.StringIO()
                with redirect_stdout(output):
                    self.assertEqual(self.track({"api_key": "key"}, name, user_id=user_id), [])
                self.assertIn("Dropping event", output.getvalue())
                self.assertNotIn("alice@example.com", output.getvalue())

    def test_events_are_not_sent_without_api_key(self):
        self.assertEqual(self.track({}, "agent_run"), [])

    def test_track_does_not_raise_when_no_thread_can_start(self):
        with mock.patch("threading.Thread.start", side_effect=RuntimeError("can't start new thread")):
            self.assertEqual(self.track({"api_key": "key"}, "agent_run"), [])

    def test_flush_waits_for_logs_and_events(self):
        sent = []

        def slow_post(url, **kwargs):
            time.sleep(0.2)
            sent.append(url)

        with mock.patch("requests.post", side_effect=slow_post), redirect_stdout(io.StringIO()):
            logdash = create_logdash({"api_key": "key", "host": "https://logdash.test"})
            logdash.logger.info("hello")
            logdash.track("agent_run")
            logdash.flush()
            self.assertCountEqual(sent, ["https://logdash.test/logs", "https://logdash.test/events"])

    def test_exit_waits_for_events(self):
        script = textwrap.dedent("""
            import time
            from unittest import mock
            from logdash import create_logdash

            def slow_post(url, **kwargs):
                time.sleep(0.2)
                print(kwargs["json"]["name"])

            mock.patch("requests.post", side_effect=slow_post).start()
            create_logdash({"api_key": "key"}).track("agent_run")
        """)
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=str(Path(__file__).resolve().parent.parent),
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.stdout, "agent_run\n", result.stderr)


if __name__ == "__main__":
    unittest.main()
