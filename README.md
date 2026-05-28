# HQC v5 vs ML-KEM Benchmarking Framework

This project consists of two major components. 
1. The resource test suite in 
    in `resource-test-suite` analyses the computational cost and memory
    usage of each KEM via `liboqs`.
2. The TLS handshake benchmark in `tls-benchmark-suite` runs an
extensive set of tests to determine how each KEM performs for key exchange.

## Conducting the tests
Each test suite has specific build configuration steps and instructions,
please see the `README.md` file in each suite's directory.

## Preparing the test server
Both tests should be conducted on a test server with runtime performance
optimization features like turbo boost disabled. The process to achieve
this is platform-specific, some example
scripts can be found in `./test-server-scripts/`
