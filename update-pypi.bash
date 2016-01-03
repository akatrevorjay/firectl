#!/usr/bin/env bash

rm -R dist/
python setup.py sdist           # source distribution
python setup.py bdist_wheel     # built package
# gpg --detach-sign -a dist/*

read -p "Password: " password
twine upload dist/* -p "$password"
