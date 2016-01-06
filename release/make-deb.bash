#!/usr/bin/env bash
OS=$1

if [[ $OS = 'debian' ]]; then
    echo 'Building deb for Debian'
    click='python3-click'
else
    echo 'Building deb for Ubuntu'
    click='python3-click-cli'
fi

fpm -s python -t deb \
    --python-bin python3 --python-pip pip3 \
    -n 'firectl' \
    -d 'firejail' \
    -d $click --no-python-dependencies \
    --after-install 'deb-postinst.sh' \
    --deb-interest '/usr/share/applications' \
    --before-remove 'deb-prerm.sh' \
    --after-remove 'deb-postrm.sh' \
    --iteration 1 \
    ../setup.py
