firectl
=======

Firectl is a tool to integrate
[firejail](https://l3net.wordpress.com/projects/firejail/) sandboxing in the
Linux desktop. Enable firejail for an application and enjoy a more secure
desktop.

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

# Restoring

Firectl works by modifying the system's desktop files, the files that tell the
system which user applications are installed and how to run them. When these
applications are updated, the desktop files are also updated, disabling
firejail. The firectl settings need to be restored.

For now you have to manually restore firejail settings after upgrades:
``` bash
sudo firectl restore
```
In the future restoring should be automatic.

# Install

Firectl can be installed with pip:
``` bash
sudo pip3 install firectl
```

# Uninstall

To uninstall firectl:
``` bash
sudo firectl disable all
sudo pip3 uninstall firectl
sudo rm /etc/firejail/firectl.conf
```
