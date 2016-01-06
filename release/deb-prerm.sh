#!/bin/sh

set -e

if [ "$1" = "remove" ]; then
    firectl disable all
fi
