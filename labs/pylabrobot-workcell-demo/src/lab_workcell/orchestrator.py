import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import TypeVar

from .devices import LiquidHandlerPort, PlateReaderPort, RetryableDeviceError
from .state import RetryPolicy, WorkcellState

T = TypeVar("T")


@dataclass
class WorkcellEvent:
  name: str
  state: WorkcellState
  detail: str | None = None


@dataclass
class WorkcellOrchestrator:
  liquid_handler: LiquidHandlerPort
  plate_reader: PlateReaderPort
  retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
  state: WorkcellState = WorkcellState.IDLE
  events: list[WorkcellEvent] = field(default_factory=list)

  def _transition(self, state: WorkcellState, detail: str | None = None) -> None:
    self.state = state
    self.events.append(WorkcellEvent(name="state_transition", state=state, detail=detail))

  async def _run_with_retry(
    self,
    operation_name: str,
    operation: Callable[[], Awaitable[T]],
  ) -> T:
    last_error: RetryableDeviceError | None = None

    for attempt in range(1, self.retry_policy.max_attempts + 1):
      try:
        return await operation()
      except RetryableDeviceError as exc:
        last_error = exc
        self._transition(
          WorkcellState.RETRYING,
          f"{operation_name}: attempt {attempt}/{self.retry_policy.max_attempts}: {exc}",
        )
        if attempt < self.retry_policy.max_attempts and self.retry_policy.delay_seconds:
          await asyncio.sleep(self.retry_policy.delay_seconds)

    assert last_error is not None
    raise last_error

  async def run(self) -> list[float]:
    if self.state not in {WorkcellState.IDLE, WorkcellState.STOPPED}:
      raise RuntimeError(f"workflow cannot start from state {self.state}")

    self._transition(WorkcellState.INITIALIZING)

    try:
      await self.liquid_handler.setup()
      await self.plate_reader.setup()
      self._transition(WorkcellState.READY)

      self._transition(WorkcellState.PIPETTING)
      await self._run_with_retry("liquid_handler.transfer_sample", self.liquid_handler.transfer_sample)

      self._transition(WorkcellState.READING)
      values = await self._run_with_retry("plate_reader.read_plate", self.plate_reader.read_plate)

      self._transition(WorkcellState.COMPLETED)
      return values
    except Exception as exc:
      self._transition(WorkcellState.FAILED, f"{type(exc).__name__}: {exc}")
      raise
    finally:
      await self._cleanup()

  async def _cleanup(self) -> None:
    cleanup_errors: list[str] = []
    for name, stop in (
      ("plate_reader", self.plate_reader.stop),
      ("liquid_handler", self.liquid_handler.stop),
    ):
      try:
        await stop()
      except Exception as exc:  # cleanup must continue for the other device
        cleanup_errors.append(f"{name}: {type(exc).__name__}: {exc}")

    if cleanup_errors:
      self.events.append(
        WorkcellEvent(
          name="cleanup_error",
          state=self.state,
          detail="; ".join(cleanup_errors),
        )
      )

    if self.state is not WorkcellState.COMPLETED and self.state is not WorkcellState.FAILED:
      self._transition(WorkcellState.STOPPED)
