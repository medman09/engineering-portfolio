#pragma once

#include <array>
#include <cstddef>
#include <cstdint>

namespace public_demo {

constexpr std::size_t kPayloadSize = 8;
using Payload = std::array<std::uint8_t, kPayloadSize>;

struct FrameMetadata {
  std::uint32_t id{};
  std::uint8_t dlc{};
  bool extended{};
  bool remote_request{};
  bool error{};
};

enum class FrameStatus {
  accepted,
  unsupported_id,
  invalid_metadata,
  invalid_dlc,
};

struct FrameValidation {
  FrameStatus status{FrameStatus::unsupported_id};
  std::uint8_t required_dlc{};
};

struct ProtocolIds {
  std::uint32_t motion_status{0x100};
  std::uint32_t system_status{0x101};
  std::uint32_t command{0x200};
};

FrameValidation validate_frame(const FrameMetadata & frame, const ProtocolIds & ids);
double decode_signed_measurement(std::uint8_t lsb, std::uint8_t msb, double scale);
Payload encode_motion_command(double velocity_mps, double steering_rad);

}  // namespace public_demo
