import os.path
import subprocess

import click

from . import config, p4, tools, ue
from .p4 import p4 as p4_grp
from .py import python as python_grp
from .ue import ue as ue_grp
from .uvs import uvs as uvs_grp
from .vstudio import vstudio as vstudio_grp


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
@click.pass_context
def cli(ctx, verbose):
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
    # it doesn't have an "update" command, so we uninstall and install
    subprocess.run(["rye", "tools", "install", "-f", "mainframe-paxo"], check=True)
    # subprocess.run("pipx upgrade mainframe-paxo", shell=True, check=True)
    print("paxo updated, now running post_update actions...")
    subprocess.run("paxo self post-update", shell=True, check=True)


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
