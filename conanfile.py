from conans import ConanFile


class GoogleTestConan(ConanFile):
    name = 'googletest'
    version = '1.7.0'
    settings = ['os', 'compiler', 'build_type', 'arch']
    generators = ['cmake']
    url = 'https://github.com/google/googletest-conan.git'
    options = {
        'BUILD_SHARED_LIBS': ['ON', 'OFF'],       # Build shared libraries (DLLs).
        'gtest_force_shared_crt': ['ON', 'OFF'],  # Use shared (DLL) run-time lib even when Google Test is built as static lib.
        'gtest_build_tests': ['ON', 'OFF'],       # Build all of gtest's own tests.
        'gtest_build_samples': ['ON', 'OFF'],     # Build gtest's sample programs.
        'gtest_disable_pthreads': ['ON', 'OFF'],  # Disable uses of pthreads in gtest.

        # Set this to 0 if your project already uses a tuple library, and GTest should use that library
        # Set this to 1 if GTest should use its own tuple library
        'GTEST_USE_OWN_TR1_TUPLE': [None, '0', '1'],

        # Set this to 0 if GTest should not use tuple at all. All tuple features will be disabled
        'GTEST_HAS_TR1_TUPLE': [None, '0'],

        # If GTest incorrectly detects whether or not the pthread library exists on your system, you can force it
        # by setting this option value to:
        #   1 - if pthread does actually exist
        #   0 - if pthread does not actually exist
        'GTEST_HAS_PTHREAD': [None, '0', '1']
    }
    default_options = ('BUILD_SHARED_LIBS=OFF',
                       'gtest_force_shared_crt=OFF',
                       'gtest_build_tests=OFF',
                       'gtest_build_samples=OFF',
                       'gtest_disable_pthreads=OFF',
                       'GTEST_USE_OWN_TR1_TUPLE=None',
                       'GTEST_HAS_TR1_TUPLE=None',
                       'GTEST_HAS_PTHREAD=None')

    build_dir = 'build'

    def source(self):
        google_test_url = 'https://github.com/google/googletest.git'
        release_tag = 'release-{version}'.format(version=self.version)
        self.run("git clone {url} --branch {branch} --depth 1".format(url=google_test_url, branch=release_tag))

    def build(self):
        option_defines = ' '.join("-D%s=%s" % (opt, val) for (opt, val) in self.options.iteritems() if val is not None)
        self.run("cmake {src_dir} -B{build_dir} {defines}".format(src_dir=self.name,
                                                                  build_dir=self.build_dir,
                                                                  defines=option_defines))
        self.run("cmake --build {build_dir}".format(build_dir=self.build_dir))

    def package(self):
        self.copy('*', dst='cmake', src="{src_dir}/cmake".format(src_dir=self.name), keep_path=True)
        self.copy('*', dst='include', src="{src_dir}/include".format(src_dir=self.name), keep_path=True)
        self.copy('CMakeLists.txt', dst='.', src=self.name, keep_path=True)

        # google mock compiles with google test sources
        self.copy('*', dst='src', src="{src_dir}/src".format(src_dir=self.name), keep_path=True)

        # Meta files
        self.copy('CHANGES', dst='.', src=self.name, keep_path=True)
        self.copy('CONTRIBUTORS', dst='.', src=self.name, keep_path=True)
        self.copy('LICENSE', dst='.', src=self.name, keep_path=True)
        self.copy('README', dst='.', src=self.name, keep_path=True)

        # Built artifacts
        self.copy('*.lib', dst='lib', src=self.build_dir, keep_path=False)
        self.copy('*.dll', dst='bin', src=self.build_dir, keep_path=False)
        if self.options['BUILD_SHARED_LIBS'] == 'ON':
            self.copy('libgtest.so', dst='lib', src=self.build_dir, keep_path=False)
            self.copy('libgtest_main.so', dst='lib', src=self.build_dir, keep_path=False)
        else:
            self.copy('libgtest.a', dst='lib', src=self.build_dir, keep_path=False)
            self.copy('libgtest_main.a', dst='lib', src=self.build_dir, keep_path=False)

        # Commented code intentionally left here
        # ======================================
        # IDE sample files
        # self.copy('*', dst='codegear', src="{src_dir}/codegear".format(src_dir=self.name))
        # self.copy('*', dst='m4', src="{src_dir}/m4".format(src_dir=self.name))
        # self.copy('*', dst='make', src="{src_dir}/make".format(src_dir=self.name))
        # self.copy('*', dst='msvc', src="{src_dir}/msvc".format(src_dir=self.name))
        # self.copy('*', dst='xcode', src="{src_dir}/xcode".format(src_dir=self.name))

        # Autoconf/Automake
        # self.copy('configure.ac', dst='configure.ac', src=self.name)
        # self.copy('Makefile.am', dst='Makefile.am', src=self.name)

        # self.copy('*', dst='samples', src="{src_dir}/samples".format(src_dir=self.name))

        # Files not used by downstream
        # self.copy('*', dst='build-aux', src="{src_dir}/build-aux".format(src_dir=self.name))
        # self.copy('*', dst='scripts', src="{src_dir}/scripts".format(src_dir=self.name))
        # self.copy('*', dst='test', src="{src_dir}/test".format(src_dir=self.name))

    def package_info(self):
        self.cpp_info.libs.append('gtest')

        if self.settings.os == 'Linux' or self.options['GTEST_HAS_PTHREAD'] == '1':
            self.cpp_info.libs.append('pthread')
