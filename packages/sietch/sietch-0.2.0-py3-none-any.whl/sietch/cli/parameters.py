"""Named Parameters for click"""

import click

name = click.option("--name", help="Name of environment", required=True)
