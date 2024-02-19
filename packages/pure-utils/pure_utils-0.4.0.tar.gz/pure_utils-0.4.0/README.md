# pure-utils

![Build Status](https://github.com/p3t3rbr0/py3-pure-utils/actions/workflows/ci.yaml/badge.svg?branch=master)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pure-utils)
![PyPI Version](https://img.shields.io/pypi/v/pure-utils)
[![Code Coverage](https://codecov.io/gh/p3t3rbr0/py3-pure-utils/graph/badge.svg?token=283H0MAGUP)](https://codecov.io/gh/p3t3rbr0/py3-pure-utils)
[![Maintainability](https://api.codeclimate.com/v1/badges/14f70c48db708a419309/maintainability)](https://codeclimate.com/github/p3t3rbr0/py3-pure-utils/maintainability)

Yet another python utilities, with the goal of collecting useful bicycles and crutches in one place ;).

Main principles:

1. No third party dependencies (standart library only).
2. Mostly pure functions without side effects.
3. Interfaces with type annotations.
4. Comprehensive documentation with examples of use.
5. Full test coverage.

**For detail information read the [doc](https://p3t3rbr0.github.io/py3-pure-utils/)**.

# Available utilities

* [common](https://p3t3rbr0.github.io/py3-pure-utils/refs/common.html) - The common purpose utilities.
  * [Singleton](https://p3t3rbr0.github.io/py3-pure-utils/refs/common.html#common.Singleton) - A metaclass that implements the singleton pattern for inheritors.
* [debug](https://p3t3rbr0.github.io/py3-pure-utils/refs/debug.html) - Utilities for debugging and development.
  * [around](https://p3t3rbr0.github.io/py3-pure-utils/refs/debug.html#debug.around) - Add additional behavior before and after execution of decorated function.
  * [caller](https://p3t3rbr0.github.io/py3-pure-utils/refs/debug.html#debug.caller) - Get the name of calling function/method (from current function/method context).
  * [deltatime](https://p3t3rbr0.github.io/py3-pure-utils/refs/debug.html#debug.deltatime) - Measure execution time of decorated function and print it to log.
  * [profileit](https://p3t3rbr0.github.io/py3-pure-utils/refs/debug.html#debug.profileit) - Profile decorated function being with 'cProfile'.
* [dt](https://p3t3rbr0.github.io/py3-pure-utils/refs/dt.html) - Utilities for working with datetime objects.
  * [apply_tz](https://p3t3rbr0.github.io/py3-pure-utils/refs/dt.html#dt.apply_tz) - Apply timezone context to datetime object.
  * [iso2format](https://p3t3rbr0.github.io/py3-pure-utils/refs/dt.html#dt.iso2format) - Convert ISO-8601 datetime string into a string of specified format.
  * [iso2dmy](https://p3t3rbr0.github.io/py3-pure-utils/refs/dt.html#dt.iso2dmy) - Convert ISO-8601 datetime string into a string of DMY (DD.MM.YYYY) format.
  * [iso2ymd](https://p3t3rbr0.github.io/py3-pure-utils/refs/dt.html#dt.iso2ymd) - Convert ISO-8601 datetime string into a string of YMD (YYYY-MM-DD) format.
  * [round_by](https://p3t3rbr0.github.io/py3-pure-utils/refs/dt.html#dt.round_by) - Round datetime, discarding excessive precision.
* [profiler](https://p3t3rbr0.github.io/py3-pure-utils/refs/profiler.html) - Helper classes for working with the cProfile.
  * [Profiler](https://p3t3rbr0.github.io/py3-pure-utils/refs/profiler.html#profiler.Profiler) - A class provides a simple interface for profiling code.
* [strings](https://p3t3rbr0.github.io/py3-pure-utils/refs/strings.html) - Utilities for working with strings.
  * [genstr](https://p3t3rbr0.github.io/py3-pure-utils/refs/strings.html#strings.genstr) - Generate ASCII-string with random letters.
  * [gzip](https://p3t3rbr0.github.io/py3-pure-utils/refs/strings.html#strings.gzip) - Compress string (or bytes string) with gzip compression level.
  * [gunzip](https://p3t3rbr0.github.io/py3-pure-utils/refs/strings.html#strings.gunzip) - Decompress bytes (earlier compressed with gzip) to string.

# License

MIT License.

Copyright (c) 2024 Peter Bro <p3t3rbr0@gmail.com || peter@peterbro.su>

See LICENSE file for more information.
