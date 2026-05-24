#! /bin/bash
PROJECT_ROOT=$(pwd)


if [ -d "_build" ]; then
    rm -rf _build
fi


mkdir _build
mkdir _build/liboqs
mkdir _build/oqs-provider

LIBOQS_REALPATH=$(realpath _build/liboqs)

echo "Cloning Liboqs..."
git clone https://github.com/diss-proj/liboqs ./_build/liboqs -b modifications --single-branch

echo "Building Liboqs..."
cd _build/liboqs

mkdir build
cd build
# The flags disable optimisation options
cmake cmake -GNinja -DOQS_ENABLE_KEM_HQC=ON -DOQS_DIST_BUILD=OFF -DOQS_OPT_TARGET=generic \
-DOQS_USE_ADX_INSTRUCTIONS=OFF \
-DOQS_USE_AES_INSTRUCTIONS=OFF \
-DOQS_USE_AVX_INSTRUCTIONS=OFF \
-DOQS_USE_AVX2_INSTRUCTIONS=OFF \
-DOQS_USE_AVX512_INSTRUCTIONS=OFF \
-DOQS_USE_BMI1_INSTRUCTIONS=OFF \
-DOQS_USE_BMI2_INSTRUCTIONS=OFF \
-DOQS_USE_PCLMULQDQ_INSTRUCTIONS=OFF \
-DOQS_USE_VPCLMULQDQ_INSTRUCTIONS=OFF \
-DOQS_USE_POPCNT_INSTRUCTIONS=OFF \
-DOQS_USE_SSE_INSTRUCTIONS=OFF \
-DOQS_USE_SSE2_INSTRUCTIONS=OFF \
-DOQS_USE_SSE3_INSTRUCTIONS=OFF \
-DOQS_USE_ARM_AES_INSTRUCTIONS=OFF \
-DOQS_USE_ARM_SHA2_INSTRUCTIONs=OFF \
-DOQS_USE_ARM_SHA3_INSTRUCTIONS=OFF \
-DOQS_USE_ARM_NEON_INSTRUCTIONS=OFF \
-DOQS_USE_OPENSSL=OFF \
..
ninja
cd $PROJECT_ROOT



echo "Cloning oqs-provider"
git clone https://github.com/diss-proj/oqs-provider _build/oqs-provider -b diss-modifications --single-branch

echo "Building oqs-provider"
cd _build/oqs-provider

liboqs_DIR="$LIBOQS_REALPATH/build"
OPENSSL_BRANCH="openssl-3.4.5"

CMAKE_PARAMS="-DCMAKE_PREFIX_PATH='$LIBOQS_REALPATH/build/src'"
source scripts/fullbuild.sh

echo "testing oqs-provider"

sleep 1

echo "project root: $PROJECT_ROOT"

cd $PROJECT_ROOT/_build/oqs-provider

echo "wd: $(pwd)"
echo "ls: $(ls)"

source scripts/runtests.sh

echo "Build completed. Libraries are in ./_build/"
