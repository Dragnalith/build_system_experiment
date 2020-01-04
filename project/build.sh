#!/bin/bash
# The script purpose is to demonstrate the build with a bash script
# Of course it will not support incremental build

# UTIL FUNCTIONS
pushd () {
    command pushd "$@" > /dev/null
}

popd () {
    command popd "$@" > /dev/null
}

# SETTING

CLANG=clang++
GCC=/usr/local/bin/g++-9

BUILD_DIR=out-build-sh
IMD_DIR="$BUILD_DIR/intermediate"
OUT_DIR="$BUILD_DIR/out"

# START
set -e
pushd $(dirname $0)

# clean & create the build directory
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR

# start compilation

imd=$IMD_DIR/clang
out=$OUT_DIR/clang
mkdir -p $imd
mkdir -p $out
$CLANG -c -o $imd/HelloWorld.o src/HelloWorld.cpp
$CLANG -g -o $out/HelloWorld $imd/HelloWorld.o

imd=$IMD_DIR/gcc
out=$OUT_DIR/gcc
mkdir -p $imd
mkdir -p $out
$GCC -c -o $imd/HelloWorld.o src/HelloWorld.cpp
$GCC -g -o $out/HelloWorld $imd/HelloWorld.o

popd