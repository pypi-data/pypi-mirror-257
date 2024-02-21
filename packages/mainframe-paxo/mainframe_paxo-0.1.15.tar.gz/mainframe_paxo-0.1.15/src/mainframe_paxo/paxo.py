import logging
import os.path
import subprocess
import tempfile
from importlib.metadata import metadata

import click
from click import echo

from . import config, log, p4, tools, ue
from .p4 import p4 as p4_grp
from .py import python as python_grp
from .ue import ue as ue_grp
from .uvs import uvs as uvs_grp
from .vstudio import vstudio as vstudio_grp

logger = logging.getLogger(__name__)


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
@click.option("--version", "-V", is_flag=True, help="Print version and exit.")
@click.pass_context
def cli(ctx, verbose, version):
    if version:
        distribution = metadata("mainframe-paxo")
        click.echo(f"{distribution['Name']} {distribution['Version']}")
        ctx.exit()
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    if verbose:
        log.init()


@cli.command()
def initial_setup():
    click.echo("Welcome to the initial setup of paxo.")
    click.echo(
        """
    Currently this is not automated.  Run the following commands:
    - paxo p4 install
    - paxo p4 setup

    Then, run the following to sync all depots:
    - paxo p4 sync

    Then, set up various UE things:
    - paxo ue setup

    """
    )


@cli.group()
def self():
    """work with paxo itself."""
    pass


@self.command()
def update():
    """Update paxo."""
    # rye manages our paxo installation
    # to self update, we must create a batch file with the instructions and launch it.abs
    bat_content = """\
@echo on
timeout 1 /nobreak >nul
rye install -f mainframe-paxo
paxo self post-update
timeout 5
"""
    # get a temporary file name to use
    filename = os.path.join(tempfile.gettempdir(), "paxo-update.bat")
    logger.info(f"Writing update bat file to {filename}")
    with open(filename, "w") as f:
        f.write(bat_content)

    # now run it, in detached mode
    # this ensures that we exit and don't get in the way of the bat file
    p = subprocess.Popen(
        f'start cmd.exe /c "{filename}"',
        shell=True,
        # ["cmd", "/c", filename],
        creationflags=subprocess.DETACHED_PROCESS,
        close_fds=True,
    )
    logger.info("%s", p)
    echo(
        "Paxo update started.  Give it a few seconds to complete, then check with 'paxo --version'"
    )


@self.command()
def post_update():
    """Run actions to refresh settings after updating paxo."""
    print("welcome to post_update_paxo")


@cli.group()
def location():
    """work with current location"""
    pass


@location.command()
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
def list(verbose):
    """list the available locations."""
    print("Available locations:")
    if not verbose:
        for location in tools.locations:
            print(f" - {location}")
    else:
        for location, info in tools.locations.items():
            print(f" - {location}")
            for key, value in info.items():
                print(f"   - {key}: {value}")


@location.command("set")
@click.option(
    "--location",
    prompt="Location",
    type=click.Choice(config.locations.keys(), case_sensitive=False),
    default=None,
)
def location_set(location):
    """set the location."""
    p4.set_location(location)
    ue.set_location(location)
    tools.location_set(location)
    print(f"Location set to {location}")


@location.command("show")
@click.pass_context
def location_show(ctx):
    """show the current location."""
    loc = tools.location_get(empty_ok=True)
    if not loc:
        print("No location set.  Did you run initial-setup?")
        return
    if ctx.obj["verbose"]:
        print(f"Current location: {loc}")
        for key, value in tools.locations[loc].items():
            print(f" - {key}: {value}")
    else:
        print(loc)


@cli.group
def subst():
    """Manage subst drive."""
    pass


@subst.command()
@click.option("--all", "-a", is_flag=True, help="Show all subst drives.")
def show(all):
    """Show the current subst drive."""
    if not all:
        drive = tools.subst_drive_get()
        echo(f"Currently configured subst drive: {drive}")
        drives = [drive]
    else:
        drives = tools.list_subst_drives().keys()
    for drive in drives:
        status = tools.check_subst_drive(drive)
        if not status["subst"]:
            print(
                "Drive {drive} currently not active.  use 'paxo subst activate' to activate it."
            )
        else:
            print(f"Drive {drive} points to folder '{status['subst']}'.")
        if not status["reg"]:
            print(
                f"Drive {drive} currently not permanently registered.  use 'paxo subst activate' to map it."
            )


@subst.command()
@click.option("--force", "-f", is_flag=True, help="Force activation.")
def activate(force):
    """Activate the subst drive."""
    tools.subst_drive(force=force)


@subst.command()
@click.option("--drive", type=str, help="deactiave a particular drive")
def deactivate(drive):
    """Deactivate the subst drive."""
    if drive:
        drive = tools.validate_drivename(drive, check_exists=True)
        tools.subst_drive(drive, deactivate=True)
    tools.subst_drive(deactivate=True)


@cli.command()
@click.option("--drive", type=click.Path(exists=True, file_okay=False, dir_okay=True))
def work_drive(drive):
    """Select or display the work drive."""
    if drive:
        drive = tools.validate_drivename(drive, check_exists=True)
        tools.workdriv_set(drive)
    else:
        drive = tools.workdrive_get(empty_ok=True)
        if not drive:
            print("No work drive set.")
            return
    print(f"Using drive {drive} as work drive.")


cli.add_command(p4_grp)
cli.add_command(ue_grp)
cli.add_command(python_grp)
cli.add_command(vstudio_grp)
cli.add_command(uvs_grp)


paxo = cli
if __name__ == "__main__":
    tools.click_main(cli, obj={})
