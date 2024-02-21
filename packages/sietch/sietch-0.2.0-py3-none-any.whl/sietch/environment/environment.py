"""Environment creation functions"""

import subprocess
import shutil
import os

import click

from ..directory import get_environment_dir


def create_environment(environment_name: str) -> None:
    """Create a new environment

    Parameters
    ----------
    environment_name : str
        The name of the environment to create
    """
    environment_path = get_environment_dir(environment_name)

    subprocess.run(["python", "-m", "venv", environment_path], check=True)


def remove_environment(environment_name: str) -> None:
    """Remove an environment

    Parameters
    ----------
    environment_name : str
        The name of the environment to remove
    """
    environment_path = get_environment_dir(environment_name)

    if os.path.exists(environment_path):
        shutil.rmtree(environment_path)


def prepare_activate_environment(environment_name: str) -> None:
    """Prepare the environment for activation

    Parameters
    ----------
    environment_name : str
        The name of the environment to activate
    """

    environment_path = get_environment_dir(environment_name)

    # Windows
    if os.name == "nt":
        activate_path = os.path.join(environment_path, "Scripts")
        command_cmd = f"{os.path.join(activate_path, 'activate')}"
        command_powershell = f"cd {activate_path} \n ,\activate"
        click.echo("Run the correct command for your shell")
        click.echo(f"Command for cmd:\n\t {command_cmd}")
        click.echo(f"Command for powershell (requires navigation):\n\t {command_powershell}")

    # Unix/Linux/Mac
    else:
        activate_path = os.path.join(environment_path, "bin", "activate")
        command = f"source {activate_path}"

        return subprocess.run(f"echo '{command}'", check=True, shell=True)
