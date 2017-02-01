#!/usr/bin/env bash

set -e
python3 -c 'import pypandoc'

rm -rf dist/
python3 setup.py sdist           # source distribution
python3 setup.py bdist_wheel     # built package
#gpg --detach-sign -a dist/firectl*.tar.gz
#gpg --detach-sign -a dist/firectl*.whl

read -s -p "Password: " password
printf "\n"
twine upload dist/* -p "$password"
