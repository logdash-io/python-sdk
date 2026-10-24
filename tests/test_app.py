import io
import threading
import unittest
from contextlib import redirect_stdout
from unittest import mock

from logdash import create_logdash


class TestApp(unittest.TestCase):
    def send_log(self, params):
        posted = threading.Event()
        with mock.patch("requests.post", side_effect=lambda *args, **kwargs: posted.set()) as post:
            with redirect_stdout(io.StringIO()):
                create_logdash(params).logger.info("hello")
            self.assertTrue(posted.wait(timeout=5), "no log was posted")
        return post.call_args.kwargs["json"]

    def send_metrics(self, params):
        with mock.patch("requests.put") as put:
            logdash = create_logdash(params)
            logdash.metrics.set("users", 1)
            logdash.metrics.mutate("logins", 1)
            logdash.flush()
        return [call.kwargs["json"] for call in put.call_args_list]

    def test_logs_carry_app(self):
        self.assertEqual(self.send_log({"api_key": "key", "app": "api"})["app"], "api")

    def test_logs_leave_out_app_when_unset(self):
        for params in ({}, {"app": None}, {"app": ""}):
            with self.subTest(params=params):
                self.assertNotIn("app", self.send_log({"api_key": "key", **params}))

    def test_metrics_carry_app(self):
        self.assertEqual(self.send_metrics({"api_key": "key", "app": "api"}), [
            {"name": "users", "value": 1, "operation": "set", "app": "api"},
            {"name": "logins", "value": 1, "operation": "change", "app": "api"},
        ])

    def test_metrics_leave_out_app_when_unset(self):
        for params in ({}, {"app": None}, {"app": ""}):
            with self.subTest(params=params):
                self.assertEqual(self.send_metrics({"api_key": "key", **params}), [
                    {"name": "users", "value": 1, "operation": "set"},
                    {"name": "logins", "value": 1, "operation": "change"},
                ])


if __name__ == "__main__":
    unittest.main()
