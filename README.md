Firectl
=======

[![License](https://img.shields.io/badge/License-GPLv2+-blue.svg)](https://github.com/rahiel/firectl/blob/master/LICENSE.txt)

**Note**: Firejail 0.9.38 has a convenient
[symlink invocation feature](https://l3net.wordpress.com/2016/02/04/firejail-0-9-38-release-announcement/)
to integrate firejail in the desktop.

Firectl is a tool to integrate [firejail](https://firejail.wordpress.com/)
sandboxing in the Linux desktop. Enable firejail for an application and enjoy a
more secure desktop.

# Usage

To see which applications can be enabled:
``` bash
firectl status
```

To enable firejail for a program:
``` bash
sudo firectl enable firefox
```

To disable firejail for a program:
``` bash
sudo firectl disable firefox
```

# Ubuntu/Debian

For Ubuntu and Debian systems install the deb at
<https://github.com/rahiel/firectl/releases>.

# Other distro's

## Restoring

Firectl works by modifying the system's desktop files, the files that tell the
system which user applications are installed and how to run them. When these
applications are updated, the desktop files are also updated, disabling
firejail. The firectl settings need to be restored.

For now you have to manually restore firejail settings after upgrades:
``` bash
sudo firectl restore
```

## Install

Install firectl with pip:
``` bash
sudo pip3 install firectl
```

## Uninstall

To uninstall firectl:
``` bash
sudo firectl disable all
sudo pip3 uninstall firectl
sudo rm /etc/firejail/firectl.conf
```
