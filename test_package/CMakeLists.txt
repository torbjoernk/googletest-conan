project(googletest-test)
cmake_minimum_required(VERSION 3.4)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(GoogleTest 1.8 REQUIRED)

add_executable(main main.cpp)
target_link_libraries(main GoogleTest::gmock_main)
