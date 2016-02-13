# Google Test Conan Build Script

This repository holds the [conan](https://www.conan.io/) build script for the [Google Test](https://github.com/google/googletest) framework.

Currently the script is configured to publish version `1.7.0` of Google Test.

## Usage

Declare the dependency.

If you are using `conanfile.txt`:
```
[requires]
googletest/1.7.0@azriel91/stable-2
```

If you are using `conanfile.py`:

```python
from conans import *

class MyProjectConan(ConanFile):
    # Either:
    requires = 'googletest/1.7.0@azriel91/stable-2'
    # Or:
    def requirements(self):
        self.requires('googletest/1.7.0@azriel91/stable-2')

    # ...
```

## Options

A full list of options and defaults can be found in [`conanfile.py`](conanfile.py)

```bash
# Example
conan install --build=missing \
              -o googletest:GTEST_USE_OWN_TR1_TUPLE=1 \
              -o googletest:GTEST_HAS_TR1_TUPLE=0
```
