"""Representative background-control pattern for a hardware-facing HMI.

This public example is intentionally device-agnostic. It demonstrates the same
engineering concerns as the private operational HMI: non-overlapping polls,
stale-result rejection, background commands, UI-thread callback handoff, and
clean shutdown.
"""

from __future__ import annotations

from dataclasses import dataclass
from queue import Empty, Queue
from threading import Lock, Thread, current_thread
from typing import Callable, Protocol


class DeviceApi(Protocol):
    """Minimal device/bridge contract used by the controller."""

    def read_status(self) -> dict[str, object]: ...


@dataclass(frozen=True)
class PollOutcome:
    generation: int
    payload: dict[str, object]
    error: str | None = None


class BackgroundController:
    """Coordinate polling and commands without blocking the UI thread.

    The caller owns the UI/event loop and periodically calls ``drain_callbacks``.
    All device I/O runs on worker threads. Only callbacks queued by this class
    are allowed to mutate UI-facing state.
    """

    def __init__(
        self,
        api: DeviceApi,
        *,
        on_status: Callable[[dict[str, object]], None],
        on_error: Callable[[str], None],
    ) -> None:
        self._api = api
        self._on_status = on_status
        self._on_error = on_error
        self._lock = Lock()
        self._callbacks: Queue[Callable[[], None]] = Queue()
        self._workers: set[Thread] = set()
        self._closing = False
        self._poll_in_flight = False
        self._generation = 0
        self._active_commands = 0
        self._refresh_requested = False

    @property
    def worker_count(self) -> int:
        with self._lock:
            return len(self._workers)

    @property
    def closing(self) -> bool:
        with self._lock:
            return self._closing

    def request_poll(self) -> bool:
        """Start one poll unless another poll/command already owns the channel."""
        with self._lock:
            if self._closing:
                return False
            if self._poll_in_flight or self._active_commands:
                self._refresh_requested = True
                return False
            self._poll_in_flight = True
            self._generation += 1
            generation = self._generation

        return self._start_worker(
            lambda: self._poll_worker(generation),
            name=f"status-poll-{generation}",
        )

    def run_command(self, command: Callable[[], None]) -> bool:
        """Run one device command and invalidate any earlier poll result."""
        with self._lock:
            if self._closing:
                return False
            self._active_commands += 1
            self._generation += 1
            self._refresh_requested = True

        return self._start_worker(
            lambda: self._command_worker(command),
            name=f"device-command-{getattr(command, '__name__', 'command')}",
        )

    def drain_callbacks(self, *, max_callbacks: int = 100) -> int:
        """Execute queued callbacks on the caller's thread."""
        processed = 0
        while processed < max_callbacks:
            try:
                callback = self._callbacks.get_nowait()
            except Empty:
                break
            callback()
            processed += 1
        return processed

    def shutdown(self) -> None:
        """Reject new work and invalidate results that return after shutdown."""
        with self._lock:
            self._closing = True
            self._generation += 1
            self._refresh_requested = False

        while True:
            try:
                self._callbacks.get_nowait()
            except Empty:
                break

    def _start_worker(self, target: Callable[[], None], *, name: str) -> bool:
        with self._lock:
            if self._closing:
                return False

        def entry() -> None:
            try:
                target()
            finally:
                with self._lock:
                    self._workers.discard(current_thread())

        worker = Thread(target=entry, name=name, daemon=True)
        with self._lock:
            if self._closing:
                return False
            self._workers.add(worker)
        worker.start()
        return True

    def _poll_worker(self, generation: int) -> None:
        try:
            outcome = PollOutcome(generation, self._api.read_status())
        except Exception as exc:
            outcome = PollOutcome(generation, {}, str(exc))
        finally:
            with self._lock:
                self._poll_in_flight = False

        self._queue_callback(lambda: self._complete_poll(outcome))

    def _complete_poll(self, outcome: PollOutcome) -> None:
        with self._lock:
            if self._closing:
                return
            is_current = outcome.generation == self._generation
            command_active = self._active_commands > 0
            refresh_requested = self._refresh_requested
            if not command_active:
                self._refresh_requested = False

        if is_current and not command_active:
            if outcome.error is None:
                self._on_status(outcome.payload)
            else:
                self._on_error(outcome.error)

        if refresh_requested and not command_active:
            self.request_poll()

    def _command_worker(self, command: Callable[[], None]) -> None:
        try:
            command()
        except Exception as exc:
            self._queue_callback(lambda message=str(exc): self._on_error(message))
        finally:
            with self._lock:
                self._active_commands = max(0, self._active_commands - 1)
            self._queue_callback(self._resume_after_command)

    def _resume_after_command(self) -> None:
        with self._lock:
            if self._closing or self._active_commands:
                return
            self._refresh_requested = False
        self.request_poll()

    def _queue_callback(self, callback: Callable[[], None]) -> bool:
        with self._lock:
            if self._closing:
                return False
            self._callbacks.put(callback)
            return True
