#! /bin/bash
# Install all necessary dependencies via apt
# Tested on Ubuntu LTS 26.04

sudo apt update

# Liboqs dependencies
sudo apt install astyle cmake gcc ninja-build libssl-dev python3-pytest python3-pytest-xdist unzip xsltproc doxygen graphviz python3-yaml valgrind
