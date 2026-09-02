import pytest

from lab_workcell import (
  FakeLiquidHandler,
  FakePlateReader,
  RetryPolicy,
  RetryableDeviceError,
  WorkcellOrchestrator,
  WorkcellState,
)


@pytest.mark.asyncio
async def test_nominal_workflow_completes_and_cleans_up() -> None:
  liquid_handler = FakeLiquidHandler()
  plate_reader = FakePlateReader(values=(0.1, 0.2, 0.3))
  orchestrator = WorkcellOrchestrator(liquid_handler, plate_reader)

  values = await orchestrator.run()

  assert values == [0.1, 0.2, 0.3]
  assert orchestrator.state is WorkcellState.COMPLETED
  assert liquid_handler.setup_calls == 1
  assert liquid_handler.transfer_calls == 1
  assert liquid_handler.stop_calls == 1
  assert plate_reader.setup_calls == 1
  assert plate_reader.read_calls == 1
  assert plate_reader.stop_calls == 1


@pytest.mark.asyncio
async def test_retryable_liquid_handler_failure_recovers() -> None:
  liquid_handler = FakeLiquidHandler(retryable_failures_before_success=1)
  plate_reader = FakePlateReader()
  orchestrator = WorkcellOrchestrator(
    liquid_handler,
    plate_reader,
    retry_policy=RetryPolicy(max_attempts=3),
  )

  values = await orchestrator.run()

  assert values
  assert liquid_handler.transfer_calls == 2
  assert orchestrator.state is WorkcellState.COMPLETED
  assert any(event.state is WorkcellState.RETRYING for event in orchestrator.events)


@pytest.mark.asyncio
async def test_retry_exhaustion_fails_and_still_cleans_up() -> None:
  liquid_handler = FakeLiquidHandler(retryable_failures_before_success=10)
  plate_reader = FakePlateReader()
  orchestrator = WorkcellOrchestrator(
    liquid_handler,
    plate_reader,
    retry_policy=RetryPolicy(max_attempts=2),
  )

  with pytest.raises(RetryableDeviceError):
    await orchestrator.run()

  assert orchestrator.state is WorkcellState.FAILED
  assert liquid_handler.transfer_calls == 2
  assert liquid_handler.stop_calls == 1
  assert plate_reader.stop_calls == 1


@pytest.mark.asyncio
async def test_workflow_cannot_restart_from_completed_state() -> None:
  orchestrator = WorkcellOrchestrator(FakeLiquidHandler(), FakePlateReader())

  await orchestrator.run()

  with pytest.raises(RuntimeError, match="cannot start"):
    await orchestrator.run()
