#include "protocol_codec.hpp"

#include <cmath>
#include <limits>
#include <stdexcept>

namespace public_demo {
namespace {
constexpr std::uint8_t kMotionStatusDlc = 4;
constexpr std::uint8_t kSystemStatusDlc = 2;
constexpr double kVelocityScale = 100.0;
constexpr double kSteeringScale = 1000.0;

std::int16_t to_scaled_int16(double value, double scale)
{
  if (!std::isfinite(value)) {
    throw std::invalid_argument("command must be finite");
  }

  const double scaled = std::round(value * scale);
  if (scaled < static_cast<double>(std::numeric_limits<std::int16_t>::min()) ||
      scaled > static_cast<double>(std::numeric_limits<std::int16_t>::max())) {
    throw std::out_of_range("command exceeds synthetic protocol range");
  }
  return static_cast<std::int16_t>(scaled);
}

void write_i16(Payload & payload, std::size_t offset, std::int16_t value)
{
  const auto raw = static_cast<std::uint16_t>(value);
  payload[offset] = static_cast<std::uint8_t>(raw & 0xFFU);
  payload[offset + 1] = static_cast<std::uint8_t>((raw >> 8U) & 0xFFU);
}
}  // namespace

FrameValidation validate_frame(const FrameMetadata & frame, const ProtocolIds & ids)
{
  if (frame.extended || frame.remote_request || frame.error) {
    return {FrameStatus::invalid_metadata, 0};
  }

  std::uint8_t required_dlc = 0;
  if (frame.id == ids.motion_status) {
    required_dlc = kMotionStatusDlc;
  } else if (frame.id == ids.system_status) {
    required_dlc = kSystemStatusDlc;
  } else {
    return {FrameStatus::unsupported_id, 0};
  }

  if (frame.dlc < required_dlc || frame.dlc > kPayloadSize) {
    return {FrameStatus::invalid_dlc, required_dlc};
  }
  return {FrameStatus::accepted, required_dlc};
}

double decode_signed_measurement(std::uint8_t lsb, std::uint8_t msb, double scale)
{
  if (!(scale > 0.0) || !std::isfinite(scale)) {
    throw std::invalid_argument("scale must be finite and positive");
  }
  const auto raw = static_cast<std::uint16_t>(
      static_cast<std::uint16_t>(msb) << 8U | lsb);
  const auto signed_raw = static_cast<std::int16_t>(raw);
  return static_cast<double>(signed_raw) / scale;
}

Payload encode_motion_command(double velocity_mps, double steering_rad)
{
  Payload payload{};
  write_i16(payload, 0, to_scaled_int16(velocity_mps, kVelocityScale));
  write_i16(payload, 2, to_scaled_int16(steering_rad, kSteeringScale));
  payload[4] = 0xA5;  // synthetic marker used only by this public demo
  return payload;
}

}  // namespace public_demo
