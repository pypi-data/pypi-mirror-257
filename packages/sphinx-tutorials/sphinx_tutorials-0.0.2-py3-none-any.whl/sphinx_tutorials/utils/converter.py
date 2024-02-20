from __future__ import annotations

from pathlib import Path

from sphinx_tutorials.utils.conversion_rules import parse_py_and_write_rst


def generate_rst(
        origin_path: Path,
        target_path: Path,
        force_overwrite: bool = False
) -> None:
    _convert_py_files(
        origin_path=origin_path,
        target_path=target_path,
        force_overwrite=force_overwrite
    )

    _create_basic_usage_rst(target_path)


def _convert_py_files(
        origin_path: Path,
        target_path: Path,
        force_overwrite: bool = False
) -> None:
    temp: list[Path] = list(origin_path.glob('**/*.py'))

    py_files: list[Path] = []
    for f in temp:
        if (  # skip files or directories starting with '_'
                str(f.relative_to(origin_path)).startswith("_")
                or f.name.startswith('_')
        ):
            continue

        py_files.append(f)

    existing_rst_files = _find_existing_rst_files(
        py_files=py_files,
        target_path=target_path,
    )

    if existing_rst_files and not force_overwrite:
        raise FileExistsError("\n\t" + "\n\t".join(map(str, existing_rst_files)))

    for f in py_files:
        rst_file = target_path / f.relative_to(origin_path).with_suffix('.rst')
        parse_py_and_write_rst(origin_file_path=f, target_file_path=rst_file)


def _find_existing_rst_files(
        py_files: list[Path],  # where the .py files are
        target_path: Path  # where the .rst should go
) -> list[str | Path]:
    out = []

    for f in py_files:

        rst_file_path = target_path / Path(f.stem).with_suffix('.rst')

        if rst_file_path.exists():
            out.append(rst_file_path)

    return out


# ----------------------------------------------------------------------

def _create_basic_usage_rst(
        target_path: Path,
        *,
        title: str = "Tutorials",
        pkg_name: str = None,
        show_versions: bool = False
) -> None:
    basic_usage_rst_path = target_path / 'basic-usage.rst'

    # get a list of all the available RST files
    rst_files = [
        file.relative_to(target_path)
        for file in target_path.glob('**/*.rst')
        if file.name != 'basic-usage.rst'
    ]

    # Create the content for 'basic-usage.rst'
    rst_content = f"{title}\n{'=' * len(title)}\n\n"

    if pkg_name is not None:
        rst_content += f"""
Tutorials to get you started using {pkg_name}.
        """

    # Add a toctree directive for all generated RST files
    rst_content += """
.. toctree::
   :maxdepth: 2
    """

    for rst_file in rst_files:
        rst_content += f"""
   {rst_file}
        """

    if show_versions:
        rst_content += f"""
    
.. code-example:: Dependencies Versions in Tutorials
    :collapsible:

    .. ipython:: python
    
        import {pkg_name}
        
        {pkg_name}.show_versions()
    
    """

    # Write the content to 'basic-usage.rst'
    with basic_usage_rst_path.open('w') as rst_file:
        rst_file.write(rst_content)
