#include "protocol_codec.hpp"

#include <cassert>
#include <cmath>
#include <iostream>
#include <stdexcept>

using namespace public_demo;

int main()
{
  const ProtocolIds ids{};

  {
    const auto result = validate_frame({ids.motion_status, 4, false, false, false}, ids);
    assert(result.status == FrameStatus::accepted);
    assert(result.required_dlc == 4);
  }
  {
    const auto result = validate_frame({0x777, 8, false, false, false}, ids);
    assert(result.status == FrameStatus::unsupported_id);
  }
  {
    const auto result = validate_frame({ids.motion_status, 2, false, false, false}, ids);
    assert(result.status == FrameStatus::invalid_dlc);
    assert(result.required_dlc == 4);
  }
  {
    const auto result = validate_frame({ids.motion_status, 4, true, false, false}, ids);
    assert(result.status == FrameStatus::invalid_metadata);
  }
  {
    const double decoded = decode_signed_measurement(0x9C, 0xFF, 100.0);
    assert(std::fabs(decoded + 1.0) < 1e-9);
  }
  {
    const auto payload = encode_motion_command(1.25, -0.250);
    assert(payload[0] == 125);
    assert(payload[1] == 0);
    assert(payload[2] == 0x06);
    assert(payload[3] == 0xFF);
    assert(payload[4] == 0xA5);
  }
  {
    bool threw = false;
    try {
      (void)encode_motion_command(std::nan(""), 0.0);
    } catch (const std::invalid_argument &) {
      threw = true;
    }
    assert(threw);
  }

  std::cout << "protocol_codec tests: PASS\n";
  return 0;
}
