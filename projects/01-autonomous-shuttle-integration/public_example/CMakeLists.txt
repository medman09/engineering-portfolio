cmake_minimum_required(VERSION 3.16)
project(public_protocol_codec_demo LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(protocol_codec protocol_codec.cpp)
target_include_directories(protocol_codec PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_compile_options(protocol_codec PRIVATE -Wall -Wextra -Wpedantic)

add_executable(test_protocol_codec test_protocol_codec.cpp)
target_link_libraries(test_protocol_codec PRIVATE protocol_codec)
target_compile_options(test_protocol_codec PRIVATE -Wall -Wextra -Wpedantic)

enable_testing()
add_test(NAME protocol_codec COMMAND test_protocol_codec)
