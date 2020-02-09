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

test/mac/test_bash.sh
test/mac/test_ninja.sh
test/mac/test_gn.sh

popd