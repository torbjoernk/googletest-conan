find_path(GOOGLETEST_INCLUDE_DIR
          NAMES gtest/gtest.h
          PATHS ${CONAN_INCLUDE_DIRS_GOOGLETEST})
find_path(GOOGLETEST_LIBRARY_DIR
          NAMES libgmock_main.a
                libgmock_main.so
                libgmock_main.lib
          PATHS ${CONAN_LIB_DIRS_GOOGLETEST})

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
                                     IMPORTED_LOCATION "${GOOGLETEST_LIBRARY_DIR}/libgmock_main.CONAN_REPLACE_LIBRARY_SUFFIX"
                                     CONAN_REPLACE_ADDITIONAL_GMOCK_PROPERTIES
                                     INTERFACE_LINK_LIBRARIES Threads::Threads)
endif()

find_package_handle_standard_args(GoogleTest
                                  REQUIRED_VARS GOOGLETEST_INCLUDE_DIR GOOGLETEST_LIBRARY_DIR
                                  VERSION_VAR GOOGLETEST_VERSION)
