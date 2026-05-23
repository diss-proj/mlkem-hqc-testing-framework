Automated testing framework to benchmark and analyse the performance
of ML-KEM vs HQC v5.0.0 for TLS 1.3 handshakes.

Consists of 5 major components:
1. Automatic Build Script
2. KEM Resource Usage Test Suite
3. TLS 1.3 Handshake Test Suite
4. Statistical Analysis Suite
5. Report/Presentation Suite

## Pre-Requisites
Building and running these benchmarks requires at least the following
dependencies:
```
astyle cmake gcc ninja-build libssl-dev python3-pytest python3-pytest-xdist
unzip xsltproc doxygen graphviz python3-yaml valgrind
```

This framework was designed and tested on Ubuntu LTS 2026.04, and includes
a script to install all necessary dependencies on Ubuntu:
`install-dependencies-ubuntu`

## 1. Building OpenSSL
`build.sh` builds OpenSSL 3.4.5, `oqs-provider` and `liboqs`
in `./_build/` for use by the test suites. A couple of key notes:
- Running `build.sh` again **deletes** `./_build` and re-builds the stack 
from source.
- The build process can be **very long**, especially on resource-limited
platforms.
- Liboqs is built **with all platform-specific optimizations disabled**,
including very common ones like AVX2.
