from __future__ import annotations

from pathlib import Path


def process_line(line, marker):
    if line.startswith(marker):
        return line[len(marker):].lstrip(), True
    return line, False


def extract_text_block(lines: list[str], start_index: int) -> tuple[str, int]:
    lines = lines[start_index:]

    end_index = 1
    while end_index < len(lines):
        if '"""' in lines[end_index]:
            break
        end_index += 1

    lines = lines[:end_index + 1]

    # Extract the text block lines, excluding the initial and final `"""`.
    text_block_str = ''.join(lines).strip().strip('"""')

    return text_block_str, end_index + 1


CLODE_BLOCKS = {
    "simple": '.. ipython:: python\n\n',
    "block": '.. code-example::\n\n    .. ipython:: python\n\n',
    "collapsible": '.. code-example::\n    :collapsible:\n\n    .. ipython:: python\n\n',
    "collapsible_open": '.. code-example::\n    :collapsible: open\n\n    .. ipython:: python\n\n',
}


def parse_py_and_write_rst(
        origin_file_path: Path,
        target_file_path: Path,
) -> None:
    with origin_file_path.open('r') as file:
        lines = file.readlines()

    rst_text = ""

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if line.startswith('"""'):
            text_block, sum_idx = extract_text_block(lines, i)
            rst_text += text_block.strip('"""') + '\n\n'
            i += sum_idx

        elif line.startswith('# -'):
            title_text, _ = process_line(line, '# -')
            if len(title_text):
                rst_text += title_text + '\n' + '-' * len(title_text) + '\n\n'

            i += 1

        elif line.startswith('# :'):
            sub_title_text, _ = process_line(line, '# :')

            if len(sub_title_text):
                rst_text += sub_title_text + '\n' + '*' * len(sub_title_text) + '\n\n'

            i += 1

        elif line.startswith('# %%'):
            sub_sub_title_text, _ = process_line(line, '# %%')

            if len(sub_sub_title_text):
                rst_text += sub_sub_title_text + '\n' + '=' * len(sub_sub_title_text) + '\n\n'

            i += 1

        else:
            if not lines[i].strip():
                i += 1
                continue

            code_block = CLODE_BLOCKS["simple"]

            title = None

            while i < len(lines) and (
                    not lines[i].startswith('"""')
                    and
                    not lines[i].startswith('# -')
                    and
                    not lines[i].startswith('# %%')
                    and
                    not lines[i].startswith('# :')
            ):

                if lines[i].startswith('# <>'):
                    title = lines[i].lstrip('# <>').strip()
                    code_block = CLODE_BLOCKS["block"]

                    if title is not None:
                        code_block = code_block.replace(
                            ".. code-example::", f".. code-example:: {title}"
                        )

                    i += 1
                    continue

                if lines[i].startswith('# collapse'):
                    code_block = CLODE_BLOCKS["collapsible"]

                    if lines[i].endswith('open'):
                        code_block = CLODE_BLOCKS["collapsible_open"]

                    if title is not None:
                        code_block = code_block.replace(
                            ".. code-example::", f".. code-example:: {title}"
                        )

                    i += 1
                    continue

                code_line = '        ' + lines[i].rstrip()
                code_block += code_line + '\n'

                i += 1

            rst_text += code_block

    target_file_path.parent.mkdir(parents=True, exist_ok=True)

    with target_file_path.open('w') as rst_file:
        rst_file.write(rst_text)
