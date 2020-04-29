#!/bin/bash

rm -rf dist build .eggs UNKNOWN.egg-info

# find . -type d -name UNKNOWN.egg-info -exec rm -rf {} \; -print

cd - > /dev/null 2>&1
