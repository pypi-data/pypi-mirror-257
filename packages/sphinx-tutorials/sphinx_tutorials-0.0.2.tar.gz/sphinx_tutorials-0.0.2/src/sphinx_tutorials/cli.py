from __future__ import annotations

import click
from pathlib import Path

from sphinx_tutorials.utils.converter import generate_rst


# Define your existing functions here

@click.group
def cli():
    pass


# main_cli.add_command(date)
@cli.command(name="to-rst")
@click.option(
    'origin_path',
    '-o',
    '--origin',
    default=Path.cwd() / "examples",
    type=click.Path(exists=True, file_okay=False)
)
@click.option(
    'target_path',
    '-t',
    '--target',
    default=Path.cwd() / "docs/basic-usage",
    type=click.Path(exists=True, file_okay=False)
)
@click.option('--overwrite', '-o', is_flag=True, help="Force overwrite existing files.")
def py_to_rst(origin_path: str | Path, target_path: str | Path, overwrite: bool):
    """
    Convert Python files in ORIGIN_PATH to reStructuredText and output to TARGET_PATH.
    """
    generate_rst(Path(origin_path), Path(target_path), force_overwrite=overwrite)
