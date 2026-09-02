from dataclasses import dataclass
from enum import StrEnum


class WorkcellState(StrEnum):
  IDLE = "idle"
  INITIALIZING = "initializing"
  READY = "ready"
  PIPETTING = "pipetting"
  READING = "reading"
  RETRYING = "retrying"
  PAUSED = "paused"
  COMPLETED = "completed"
  FAILED = "failed"
  STOPPED = "stopped"


@dataclass(frozen=True)
class RetryPolicy:
  max_attempts: int = 3
  delay_seconds: float = 0.0

  def __post_init__(self) -> None:
    if self.max_attempts < 1:
      raise ValueError("max_attempts must be at least 1")
    if self.delay_seconds < 0:
      raise ValueError("delay_seconds cannot be negative")
