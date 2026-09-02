from dataclasses import dataclass
from typing import Protocol


class RetryableDeviceError(RuntimeError):
  """Temporary device failure for which a bounded retry may be appropriate."""


class PermanentDeviceError(RuntimeError):
  """Non-retryable device failure requiring operator or engineering action."""


class LiquidHandlerPort(Protocol):
  async def setup(self) -> None: ...
  async def transfer_sample(self) -> None: ...
  async def stop(self) -> None: ...


class PlateReaderPort(Protocol):
  async def setup(self) -> None: ...
  async def read_plate(self) -> list[float]: ...
  async def stop(self) -> None: ...


@dataclass
class FakeLiquidHandler:
  retryable_failures_before_success: int = 0
  setup_calls: int = 0
  transfer_calls: int = 0
  stop_calls: int = 0

  async def setup(self) -> None:
    self.setup_calls += 1

  async def transfer_sample(self) -> None:
    self.transfer_calls += 1
    if self.transfer_calls <= self.retryable_failures_before_success:
      raise RetryableDeviceError("simulated liquid-handler timeout")

  async def stop(self) -> None:
    self.stop_calls += 1


@dataclass
class FakePlateReader:
  values: tuple[float, ...] = (0.12, 0.18, 0.24, 0.31)
  retryable_failures_before_success: int = 0
  setup_calls: int = 0
  read_calls: int = 0
  stop_calls: int = 0

  async def setup(self) -> None:
    self.setup_calls += 1

  async def read_plate(self) -> list[float]:
    self.read_calls += 1
    if self.read_calls <= self.retryable_failures_before_success:
      raise RetryableDeviceError("simulated plate-reader timeout")
    return list(self.values)

  async def stop(self) -> None:
    self.stop_calls += 1
