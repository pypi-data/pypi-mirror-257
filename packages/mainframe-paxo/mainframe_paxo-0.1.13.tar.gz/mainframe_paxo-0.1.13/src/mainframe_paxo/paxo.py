import os.path
import subprocess
import tempfile
from importlib.metadata import metadata

import click

from . import config, p4, tools, ue
from .p4 import p4 as p4_grp
from .py import python as python_grp
from .ue import ue as ue_grp
from .uvs import uvs as uvs_grp
from .vstudio import vstudio as vstudio_grp


@click.group(invoke_without_command=True)
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
@click.option("--version", "-V", is_flag=True, help="Print version and exit.")
@click.pass_context
def cli(ctx, verbose, version):
    if version:
        distribution = metadata("mainframe-paxo")
        click.echo(f"{distribution['Name']} {distribution['Version']}")
        return
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


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
    # tot self updatte, we must create a batch file with the instructions and launch it.abs
    bat_content = """\
@echo on
timeout 1 /nobreak >nul
rye install -f mainframe-paxo
paxo self post-update
"""
    # get a temporary file name to use
    filename = os.path.join(tempfile.gettempdir(), "paxo-update.bat")
    with open(filename, "w") as f:
        f.write(bat_content)

    # now run it, in detached mode
    # this ensures that we exit and don't gett in the way of the bat file
    subprocess.Popen(
        ["cmd", "/c", filename],
        creationflags=subprocess.DETACHED_PROCESS,
        close_fds=True,
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


@cli.command()
@click.option("--drive", type=click.Path(exists=False))
def subst_drive(drive):
    """Select or display the subst drive."""
    if drive:
        drive = tools.validate_drivename(drive, check_exists=False)
        tools.subst_drive_set(drive)
    else:
        drive = tools.subst_drive_get()
        print(f"Current subst drive: {drive}")
    print(f"Using drive {drive} as subst drive for {config.work_drive_dev_folder}")
    if not os.path.isfile(drive):
        print("currently not subst")


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
