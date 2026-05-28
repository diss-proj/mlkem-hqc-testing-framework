# KEM Resource Usage Test Suite
This test measures the computtaional cost, execution time, and memory usage
of each KEM's KeyGen(), Encaps() and Decaps() algorithms. It's designed
to be run on effectively any platform, including low-powered computers like
Raspbery Pis.

## Pre-Requisites
### Dependencies
Ensure you've installed all necessary dependencies to build the cryptographic
libraries necessary for this test suite. 
`<PROJECT-ROOT>/test-server-scripts/install-dependencies.sh` will
download and install them via apt if you're on Ubuntu LTS 26.04 or similar.

### Memory
Building the libraries for this test suite requires more than 1 GiB of RAM,
which presents an issue for low-powered systems. 
`<PROJECT-ROOT>/test-server-scripts/swapspace.sh` will create and activate
a 2GiB swap file to enable those systems to build the project. Please note
that building this project's libraries on a low-powered device may take
approximately 1 hour.

## Building
### Configruation
By default, this project is configured to build specifically modified
versions of `liboqs` and `oqs-provider` with all platform-specific
optimizations disabled. You can re-enable platform optimizations by
altering the `-DOQS_USE_X_INSTRUCTIONS` flags in `build.sh`.

The build script will build local copies of OpenSSL, `oqs-provider`
and `liboqs` in `./_build/`, and will not install them system-wide.

### Build Script
Run `sudo ./build.sh` to build this test suite's libraries from source,
which may take some time.

## Running the tests
The test suite is defined in `kem-resource-test-suite.py`.
### Configuration
By deafult, the test suite analyses each KEM's speed by timing how many
executions of `KeyGen()`, `Encaps()` or `Decaps()` it can complete in
a 30-second window. The duration of each test window is defined by 
the `SPEEDTEST_DURATION` variable at the top of the script.

## Results
Each batch of tests is stored in a timestamped directory under
`./resource-test-results`. 
