from conans import ConanFile, CMake, tools
import os


class GoogleTestConan(ConanFile):
    name = 'googletest'
    description = 'GoogleTest with GoogleMock'
    license = 'Copyright 2008, Google Inc.'  # See https://github.com/google/googletest/blob/release-1.8.0/googletest/LICENSE
    version = '1.8.0'
    release_version = 'release-{ver}'.format(ver=version)
    settings = ['os', 'compiler', 'build_type', 'arch']
    generators = ['cmake']
    url = 'https://github.com/astrohawk/googletest-conan.git'
    options = {
        'static': [True, False],
        'shared_crt': [True, False]
    }
    default_options = (
        'static=True',
        'shared_crt=True'
    )
    exports = ['FindGoogleTest.cmake']

    src_dir = '{n}-{release_ver}'.format(n=name, release_ver=release_version)
    build_dir = 'build'

    def source(self):
        if not os.path.isdir("{conan_dir}{sep}{src_dir}".format(conan_dir=self.conanfile_directory, sep=os.sep, src_dir=self.src_dir)):
            zip_name = '{release_version}.zip'.format(release_version=self.release_version)
            url = 'https://github.com/google/googletest/archive/{zip}'.format(zip=zip_name)
            self.output.info("Downloading %s" % zip_name)
            tools.download(url, zip_name)
            tools.unzip(zip_name)
            os.unlink(zip_name)

    def build(self):
        self.source()

        static = "-DBUILD_SHARED_LIBS=%s" % ("OFF" if self.options.static else "ON")
        shared_crt = '-Dgtest_force_shared_crt=%s' % ('ON' if self.options.shared_crt else 'OFF')

        cmake = CMake(self.settings)
        cmd_line = 'cmake "%s" -B%s %s %s %s' % (self.src_dir, self.build_dir, cmake.command_line, static, shared_crt)
        self.output.info("CMake Command: %s" % cmd_line)
        self.run(cmd_line)

        cmd_line = 'cmake --build "%s" %s' % (self.build_dir, cmake.build_config)
        self.output.info("CMake Command: %s" % cmd_line)
        self.run(cmd_line)

    def package(self):
        # Headers
        self.copy('*.h', dst='include', src="{src_dir}/googletest/include".format(src_dir=self.src_dir), keep_path=True)
        self.copy('*.h', dst='include', src="{src_dir}/googlemock/include".format(src_dir=self.src_dir), keep_path=True)

        # Custom CMake Find Module
        self._patch_cmake_find_module()
        self.copy('FindGoogleTest.cmake', dst='.', src='.')

        # Meta files
        self.copy('CHANGES', dst='.', src="%s/googletest" % self.src_dir, keep_path=True)
        self.copy('CONTRIBUTORS', dst='.', src="%s/googletest" % self.src_dir, keep_path=True)
        self.copy('LICENSE', dst='.', src="%s/googletest" % self.src_dir, keep_path=True)
        self.copy('README', dst='.', src="%s/googletest" % self.src_dir, keep_path=True)

        # Built artifacts
        if self.settings.os == "Linux":
            if self.options.static:
                self.copy('*.a', dst='lib', src=self.build_dir, keep_path=False)
            else:
                self.copy('*.so', dst='lib', src=self.build_dir, keep_path=False)
        elif self.settings.os == "Windows":
            if not self.options.static:
                self.copy('*.dll', dst='bin', src=self.build_dir, keep_path=False)
            self.copy('*.lib', dst='lib', src=self.build_dir, keep_path=False)
        else:
            raise NotImplementedError("Operating System not (yet) supported: %s" % self.settings.os)

    def package_info(self):
        self.cpp_info.libs = ['gtest', 'gtest_main', 'gmock', 'gmock_main']
        if self.settings.os == "Linux":
            self.cpp_info.libs = ['lib%s' % lib for lib in self.cpp_info.libs]
            if self.options.static:
                self.cpp_info.libs = ['%s.a' % lib for lib in self.cpp_info.libs]
            else:
                self.cpp_info.libs = ['%s.so' % lib for lib in self.cpp_info.libs]

    def _patch_cmake_find_module(self):
        tools.replace_in_file('FindGoogleTest.cmake',
                              'CONAN_REPLACE_SHARED_OR_STATIC',
                              'STATIC' if self.options.static else 'SHARED')
        tools.replace_in_file('FindGoogleTest.cmake',
                              'CONAN_REPLACE_VERSION',
                              '%s' % self.version)

        if self.options.static:
            _interface_compile_definitions = None
        else:
            _interface_compile_definitions = 'GTEST_LINKED_AS_SHARED_LIBRARY=1'

        if self.settings.os == "Linux":
            _library_name = '${GOOGLETEST_LIBRARY_DIR}/libgmock_main.' + 'a' if self.options.static else 'so'
            _import_library_name = None
            _interface_link_libraries = "Threads::Threads"
        elif self.settings.os == "Windows":
            _interface_link_libraries = None
            if self.options.static:
                _library_name = '${GOOGLETEST_LIBRARY_DIR}/gmock_main.lib'
                _import_library_name = None
            else:
                _library_name = '${GOOGLETEST_BINARY_DIR}/gmock_main.dll'
                _import_library_name = '${GOOGLETEST_LIBRARY_DIR}/gmock_main.lib'
        else:
            raise NotImplementedError("Operating System not (yet) supported: %s" % self.settings.os)

        tools.replace_in_file('FindGoogleTest.cmake',
                              'CONAN_REPLACE_IMPORTED_LOCATION',
                              ('IMPORTED_LOCATION "%s"' % _library_name) if _library_name else '')
        tools.replace_in_file('FindGoogleTest.cmake',
                              'CONAN_REPLACE_IMPORTED_IMPLIB',
                              ('IMPORTED_IMPLIB "%s"' % _import_library_name) if _import_library_name else '')
        tools.replace_in_file('FindGoogleTest.cmake',
                              'CONAN_REPLACE_INTERFACE_COMPILE_DEFINITIONS',
                              ('INTERFACE_COMPILE_DEFINITIONS %s' % _interface_compile_definitions) if _interface_compile_definitions else '')
        tools.replace_in_file('FindGoogleTest.cmake',
                              'CONAN_REPLACE_INTERFACE_LINK_LIBRARIES',
                              ('INTERFACE_LINK_LIBRARIES %s' % _interface_link_libraries) if _interface_link_libraries else '')
