# -*- coding: utf-8 -*-
import os

import click

profile_path = "/etc/firejail/"
application_path = "/usr/share/applications/"

profiles = [os.path.splitext(f)[0] for f in os.listdir(profile_path)]
applications = [os.path.splitext(f)[0] for f in os.listdir(application_path)]
installed = [os.path.join(application_path, a + ".desktop")
             for a in profiles if a in applications]


@click.group()
def cli():
    pass


def get_desktop(program):
    """Get path to program's desktop file."""
    path = os.path.join(application_path, program + ".desktop")
    if os.path.isfile(path):
        return path
    else:
        raise click.ClickException(
            "Desktop file for %s does not exist." % program)


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


def check_programs(program):
    """Return list of programs to enable / disable."""
    if len(program) == 0:
        raise click.ClickException("No program specified.")

    # Check if we have permission to modify global desktop files.
    if not os.access(installed[0], os.W_OK):
        raise click.UsageError(
            message="Can't modify desktop files, please execute as root.")

    if program[0] == "all":
        program = installed
    else:
        program = [get_desktop(p) for p in program]
    return program


@cli.command(help="enable firejail for program")
@click.argument("program", type=click.STRING, nargs=-1)
def enable(program):
    """Enable firejail for program."""
    programs = check_programs(program)

    for p in programs:
        replace(p,
                lambda l: l.startswith("Exec=") and "firejail" not in l,
                lambda l: "Exec=firejail " + l[l.find('=') + 1:])


@cli.command(help="disable firejail for program")
@click.argument("program", type=click.STRING, nargs=-1)
def disable(program):
    """Disable firejail for program."""
    programs = check_programs(program)

    for p in programs:
        replace(p,
                lambda line: line.startswith("Exec=firejail"),
                lambda line: "Exec=" + line[14:])


@cli.command(help="show status of firejail profiles")
def status():
    """Display status of available firejail profiles."""
    enabled = []
    disabled = []
    for p in installed:
        name = os.path.splitext(os.path.basename(p))[0]
        with open(p, 'r') as f:
            if "Exec=firejail" in f.read():
                enabled.append(name)
            else:
                disabled.append(name)

    click.echo("%d firejail profiles are enabled" % len(enabled))
    for p in sorted(enabled):
        click.echo("   %s" % p)

    click.echo("%d firejail profiles are available and disabled" % len(disabled))
    for p in sorted(disabled):
        click.echo("   %s" % p)


if __name__ == "__main__":
    cli()
