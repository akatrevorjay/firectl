# -*- coding: utf-8 -*-
__version__ = "1.0"

import os
from difflib import get_close_matches

import click


profile_path = "/etc/firejail/"
application_path = "/usr/share/applications/"
config = "/etc/firejail/firectl.conf"

profiles = [os.path.splitext(f)[0] for f in os.listdir(profile_path)]
applications = [os.path.splitext(f)[0] for f in os.listdir(application_path)]
installed = [p for p in profiles if p in applications]


@click.version_option()
@click.group()
def cli():
    pass


def get_config():
    """Get header and config."""
    header = "# list of enforced firejail profiles\n"
    try:
        with open(config, 'r') as f:
            conf = [l.strip() for l in f.readlines() if not l.startswith('#')]
    except FileNotFoundError:
        conf = []
    return header, conf


def write_config(programs, test, combine):
    """Write config to disk if necessary. Uses test to check if a program has to
    be added/removed from the config. Programs and conf are combined with
    combine.
    """
    header, conf = get_config()
    programs = [os.path.splitext(os.path.basename(p))[0] for p in programs]

    write = False
    for p in programs:
        if test(p, conf):
            write = True
            continue

    if write:
        lines = header + "\n".join(sorted(combine(programs, conf)))
        with open(config, 'w') as f:
            f.writelines(lines)


def add_config(programs):
    """Add programs to config."""
    write_config(programs,
                 lambda program, conf: program not in conf,
                 lambda programs, conf: set(conf + programs))


def remove_config(programs):
    """Remove programs from config."""
    write_config(programs,
                 lambda program, conf: program in conf,
                 lambda programs, conf: set(conf) - set(programs))


def get_desktop(program):
    """Get path to program's desktop file."""
    path = os.path.join(application_path, program + ".desktop")
    if os.path.isfile(path):
        return path
    else:
        message = "Desktop file for %s does not exist." % program

        typo = get_close_matches(program, installed, n=1)
        if len(typo) > 0:
            message += "\n\nDid you mean %s?" % typo[0]

        raise click.ClickException(message)


def replace(filename, condition, transform):
    """Replace lines in filename for which condition is true with transform."""
    newfile = []
    with open(filename, 'r') as f:
        for line in f:
            if condition(line):
                newfile.append(transform(line))
            else:
                newfile.append(line)

    with open(filename, 'w') as f:
        f.writelines(newfile)


def get_programs(program):
    """Return list of programs to enable / disable."""
    if len(program) == 0:
        raise click.ClickException("No program specified.")

    # Check if we have permission to modify global desktop files.
    if not os.access(get_desktop(installed[0]), os.W_OK):
        raise click.UsageError(
            message="Can't modify desktop files, please execute as root.")

    if program[0] == "all":
        program = installed

    return [get_desktop(p) for p in program]


@cli.command(help="enable firejail for program")
@click.argument("program", type=click.STRING, nargs=-1)
def enable(program, update_config=True):
    """Enable firejail for program. Program is tuple/list of program names."""
    programs = get_programs(program)

    for p in programs:
        replace(p,
                lambda l: l.startswith("Exec=") and "firejail" not in l,
                lambda l: "Exec=firejail " + l[l.find('=') + 1:])

    if update_config:
        add_config(programs)


@cli.command(help="disable firejail for program")
@click.argument("program", type=click.STRING, nargs=-1)
def disable(program):
    """Disable firejail for program. Program is tuple/list of program names."""
    programs = get_programs(program)

    for p in programs:
        replace(p,
                lambda line: line.startswith("Exec=firejail"),
                lambda line: "Exec=" + line[14:])

    remove_config(programs)


@cli.command(help="show status of firejail profiles")
def status():
    """Display status of available firejail profiles."""
    enabled = []
    disabled = []
    for p in installed:
        with open(get_desktop(p), 'r') as f:
            if "Exec=firejail" in f.read():
                enabled.append(p)
            else:
                disabled.append(p)

    header, conf = get_config()
    update_disabled = [p for p in conf if p not in enabled]
    disabled = [p for p in disabled if p not in update_disabled]

    click.echo("{:<2} firejail profiles are enabled".format(len(enabled)))
    for p in sorted(enabled):
        click.echo("   %s" % p)
    print()

    click.echo("{:<2} firejail profiles are disabled and available"
               .format(len(disabled)))
    for p in sorted(disabled):
        click.echo("   %s" % p)

    if len(update_disabled) > 0:
        click.secho("\n{} firejail profiles are disabled by updates"
                    .format(len(update_disabled)), fg="red")
        for p in sorted(update_disabled):
            click.echo("   %s" % p)
        click.echo("Please run: sudo firectl restore")


@cli.command(help="restore firejail profiles from config")
def restore():
    """Re-enable firejail profiles for when desktop files get updated."""
    header, conf = get_config()

    # clean config from enabled programs removed from the system
    removed = [c for c in conf if c not in installed]
    remove_config(removed)
    [conf.remove(c) for c in removed]

    if len(conf) > 0:
        enable.callback(conf, update_config=False)
