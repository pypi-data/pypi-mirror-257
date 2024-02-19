"""Functions related to file operations"""

from os.path import join, abspath, expanduser
from os import environ, makedirs, walk


def get_sietch_dir() -> str:
    """Get the directory where sietch environments are installed

    Returns
    -------
    str
        The directory where sietch environments are installed
    """

    if "SIETCH_HOME" in environ:
        return environ["SIETCH_HOME"]
    else:
        return abspath(join(expanduser("~"), ".sietch"))


def create_sietch_dir() -> None:
    """Create the sietch directory if it doesn't exist"""

    sietch_dir = get_sietch_dir()
    if not sietch_dir.exists():
        makedirs(sietch_dir)


def get_environment_dir(environment_name: str) -> str:
    """Get the directory for the specified environment

    Parameters
    ----------
    environment_name : str
        The name of the environment

    Returns
    -------
    str
        The directory for the specified environment
    """

    return join(get_sietch_dir(), environment_name)


def create_environment_dir(environment_name: str) -> None:
    """Create the directory for the specified environment

    Parameters
    ----------
    environment_name : str
        The name of the environment
    """

    environment_dir = get_environment_dir(environment_name)
    if not environment_dir.exists():
        makedirs(environment_dir)


def list_environments() -> list:
    """List all environments

    Returns
    -------
    list[str]
        A list of all environments
    """

    envs = [x for x in next(walk(get_sietch_dir()))[1]]

    return envs
