#!/bin/bash

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

rm -rf dist build .eggs UNKNOWN.egg-info


cd - > /dev/null 2>&1
