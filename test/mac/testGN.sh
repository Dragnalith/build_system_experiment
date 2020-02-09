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

# START
set -e
pushd $(dirname $0)

rm -rf ../../out/build-gn
../../bin/mac/gn --root=../../project -q gen ../../out/build-gn
../../bin/mac/ninja -C ../../out/build-gn

popd