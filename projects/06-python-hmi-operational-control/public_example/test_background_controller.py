import time
import unittest
from threading import Event

from background_controller import BackgroundController


def wait_until(predicate, timeout=1.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.005)
    return predicate()


class FakeApi:
    def __init__(self):
        self.calls = 0
        self.block = Event()
        self.block.set()
        self.payload = {"state": "READY"}
        self.error = None

    def read_status(self):
        self.calls += 1
        self.block.wait(timeout=1.0)
        if self.error:
            raise RuntimeError(self.error)
        return dict(self.payload)


class BackgroundControllerTests(unittest.TestCase):
    def setUp(self):
        self.api = FakeApi()
        self.statuses = []
        self.errors = []
        self.controller = BackgroundController(
            self.api,
            on_status=self.statuses.append,
            on_error=self.errors.append,
        )

    def tearDown(self):
        self.controller.shutdown()
        wait_until(lambda: self.controller.worker_count == 0)

    def pump(self):
        self.controller.drain_callbacks()

    def test_nominal_poll_delivers_status(self):
        self.assertTrue(self.controller.request_poll())
        self.assertTrue(wait_until(lambda: self.controller.worker_count == 0))
        self.pump()
        self.assertEqual(self.statuses, [{"state": "READY"}])
        self.assertEqual(self.errors, [])

    def test_overlapping_poll_is_rejected_and_coalesced(self):
        self.api.block.clear()
        self.assertTrue(self.controller.request_poll())
        self.assertFalse(self.controller.request_poll())
        self.assertEqual(self.api.calls, 1)
        self.api.block.set()
        self.assertTrue(wait_until(lambda: self.controller.worker_count == 0))
        self.pump()
        self.assertTrue(wait_until(lambda: self.controller.worker_count == 0))
        self.pump()
        self.assertEqual(self.api.calls, 2)

    def test_command_invalidates_stale_poll_result(self):
        self.api.block.clear()
        self.assertTrue(self.controller.request_poll())
        self.assertTrue(wait_until(lambda: self.api.calls == 1))

        command_done = Event()
        self.assertTrue(self.controller.run_command(command_done.set))
        self.assertTrue(wait_until(command_done.is_set))

        self.api.payload = {"state": "AFTER_COMMAND"}
        self.api.block.set()
        self.assertTrue(wait_until(lambda: self.controller.worker_count == 0))
        self.pump()
        self.assertTrue(wait_until(lambda: self.controller.worker_count == 0))
        self.pump()

        self.assertEqual(self.statuses, [{"state": "AFTER_COMMAND"}])

    def test_poll_error_is_reported(self):
        self.api.error = "bridge offline"
        self.controller.request_poll()
        self.assertTrue(wait_until(lambda: self.controller.worker_count == 0))
        self.pump()
        self.assertEqual(self.errors, ["bridge offline"])

    def test_shutdown_rejects_new_work_and_discards_callbacks(self):
        self.controller.shutdown()
        self.assertFalse(self.controller.request_poll())
        self.assertFalse(self.controller.run_command(lambda: None))
        self.assertEqual(self.controller.drain_callbacks(), 0)


if __name__ == "__main__":
    unittest.main()
