#!/bin/sh

set -e

if [ "$1" = "triggered" ]; then
    firectl restore
fi
