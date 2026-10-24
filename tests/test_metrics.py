import io
import os
import subprocess
import sys
import textwrap
import threading
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from logdash import create_logdash


class TestMetrics(unittest.TestCase):
    def stored(self, operations, delay=0.0):
        """Run metric operations against a server that applies them in the order they arrive."""
        values = {}

        def put(url, json, **kwargs):
            time.sleep(delay)
            name, value = json["name"], json["value"]
            values[name] = value if json["operation"] == "set" else values.get(name, 0) + value

        with mock.patch("requests.put", side_effect=put):
            logdash = create_logdash({"api_key": "key"})
            for method, name, value in operations:
                getattr(logdash.metrics, method)(name, value)
            logdash.flush()
        return values

    def test_metrics_do_not_block_the_caller(self):
        with mock.patch("requests.put", side_effect=lambda *args, **kwargs: time.sleep(0.5)) as put:
            logdash = create_logdash({"api_key": "key"})
            started = time.monotonic()
            logdash.metrics.set("users", 1)
            logdash.metrics.mutate("logins", 1)
            self.assertLess(time.monotonic() - started, 0.1)
            logdash.flush()
        self.assertEqual(put.call_count, 2)

    def test_metrics_end_at_the_values_of_their_operations_in_order(self):
        operations, expected = [], {}
        for i in range(300):
            name = ("users", "logins", "errors")[i % 3]
            if i % 7 == 0:
                operations.append(("set", name, i))
                expected[name] = i
            else:
                operations.append(("mutate", name, 1))
                expected[name] = expected.get(name, 0) + 1
        self.assertEqual(self.stored(operations, delay=0.001), expected)

    def test_operations_behind_a_request_merge_like_the_server_merges_them(self):
        on_the_wire, release, sent = threading.Event(), threading.Event(), []

        def put(url, json, **kwargs):
            sent.append((json["operation"], json["value"]))
            on_the_wire.set()
            release.wait(5)

        with mock.patch("requests.put", side_effect=put):
            logdash = create_logdash({"api_key": "key"})
            logdash.metrics.set("users", 0)
            self.assertTrue(on_the_wire.wait(5))
            logdash.metrics.mutate("users", 1)
            logdash.metrics.set("users", 5)
            logdash.metrics.mutate("users", 2)
            time.sleep(0.1)
            self.assertEqual(sent, [("set", 0)], "a request went out before the one on the wire finished")
            release.set()
            logdash.flush()
        self.assertEqual(sent, [("set", 0), ("set", 7)])

    def test_a_metric_waits_for_the_next_one_when_no_thread_can_start(self):
        with mock.patch("requests.put") as put:
            logdash = create_logdash({"api_key": "key"})
            with mock.patch("threading.Thread.start", side_effect=RuntimeError("can't start new thread")):
                logdash.metrics.set("users", 1)
            logdash.metrics.mutate("users", 1)
            logdash.flush()
        self.assertEqual([call.kwargs["json"] for call in put.call_args_list], [{"name": "users", "value": 2, "operation": "set"}])

    def test_numeric_strings_are_numbers(self):
        self.assertEqual(self.stored([("set", "users", "41"), ("mutate", "users", 1)]), {"users": 42})

    def test_invalid_values_are_dropped_with_a_warning(self):
        output = io.StringIO()
        with redirect_stdout(output):
            values = self.stored([("set", "users", value) for value in ("many", None, float("nan"), float("inf"), 10 ** 400)])
        self.assertEqual(values, {})
        self.assertEqual(output.getvalue().count("Dropping metric"), 5)

    @unittest.skipUnless(hasattr(os, "fork"), "needs os.fork")
    def test_a_forked_child_sends_its_own_metrics(self):
        script = textwrap.dedent("""
            import os
            import threading
            import time
            from unittest import mock
            from logdash import create_logdash

            parent = os.getpid()
            on_the_wire = threading.Event()

            def slow_put(url, json, **kwargs):
                on_the_wire.set()
                time.sleep(0.3)
                # One write per line, so the parent's and the child's lines cannot interleave
                os.write(1, f"{'parent' if os.getpid() == parent else 'child'} {json['name']}\\n".encode())

            mock.patch("requests.put", side_effect=slow_put).start()
            logdash = create_logdash({"api_key": "key"})
            logdash.metrics.set("before_fork", 1)
            on_the_wire.wait(5)
            if os.fork() == 0:
                logdash.metrics.set("in_child", 1)
                logdash.flush()
                os._exit(0)
            os.wait()
        """)
        result = subprocess.run(
            [sys.executable, "-W", "ignore", "-c", script],
            cwd=str(Path(__file__).resolve().parent.parent),
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(sorted(result.stdout.splitlines()), ["child in_child", "parent before_fork"], result.stderr)


if __name__ == "__main__":
    unittest.main()
