include(FindPackageHandleStandardArgs)

find_path(GOOGLETEST_INCLUDE_DIR
          NAMES gtest/gtest.h
          PATHS ${CONAN_INCLUDE_DIRS_GOOGLETEST})
find_path(GOOGLETEST_LIBRARY_DIR
          NAMES libgmock_main.a
                libgmock_main.so
                gmock_main.lib
          PATHS ${CONAN_LIB_DIRS_GOOGLETEST})
find_path(GOOGLETEST_BINARY_DIR
          NAMES gmock_main.dll
          PATHS ${CONAN_BIN_DIRS_GOOGLETEST})

set(GOOGLETEST_VERSION CONAN_REPLACE_VERSION)
set(GOOGLETEST_INCLUDE_DIRS ${GOOGLETEST_INCLUDE_DIR})

if(${UNIX})
    set(THREADS_PREFER_PTHREAD_FLAG TRUE)
    find_package(Threads REQUIRED)
endif()

if(NOT TARGET GoogleTest::gmock_main)
    add_library(GoogleTest::gmock_main CONAN_REPLACE_SHARED_OR_STATIC IMPORTED GLOBAL)
    set_target_properties(GoogleTest::gmock_main
                          PROPERTIES INTERFACE_INCLUDE_DIRECTORIES ${GOOGLETEST_INCLUDE_DIR}
                                     IMPORTED_LINK_INTERFACE_LANGUAGES "CXX"
                                     CONAN_REPLACE_IMPORTED_LOCATION
                                     CONAN_REPLACE_IMPORTED_IMPLIB
                                     CONAN_REPLACE_INTERFACE_COMPILE_DEFINITIONS
                                     CONAN_REPLACE_INTERFACE_LINK_LIBRARIES)
endif()

find_package_handle_standard_args(GoogleTest
                                  REQUIRED_VARS GOOGLETEST_INCLUDE_DIR GOOGLETEST_LIBRARY_DIR
                                  VERSION_VAR GOOGLETEST_VERSION)
