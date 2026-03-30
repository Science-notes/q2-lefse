import os
import shlex
import shutil
import subprocess
import tempfile
from typing import Optional

from ._otu import OTUTableFormat


class LefseError(RuntimeError):
    """Raised when a LEfSe command fails."""


def _resolve_prefix(command_prefix: str) -> list:
    """Resolve LEfSe execution prefix.

    Priority:
    1) method/visualizer parameter ``command_prefix``
    2) env var ``Q2_LEFSE_COMMAND_PREFIX``
    3) empty (run directly in current env)
    """
    prefix = command_prefix.strip() if command_prefix else ''
    if not prefix:
        prefix = os.environ.get('Q2_LEFSE_COMMAND_PREFIX', '').strip()
    return shlex.split(prefix) if prefix else []


def _run_command(cmd):
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError as e:
        raise LefseError(
            f"Command not found: {cmd[0]}. Please install lefse (Python 2.7 env) and ensure command prefix is correct."
        ) from e
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.strip() if e.stderr else ''
        stdout = e.stdout.strip() if e.stdout else ''
        message = '\n'.join(part for part in [stdout, stderr] if part)
        raise LefseError(
            f"LEfSe command failed: {' '.join(cmd)}\n{message}"
        ) from e


def _lefse_cmd(prefix: list, script: str, args: list) -> list:
    return prefix + [script] + args


def run(
    otu_table: OTUTableFormat,
    class_id: int,
    subclass_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    normalization: int = 1000000,
    lda_threshold: float = 2.0,
    wilcoxon_alpha: float = 0.05,
    kruskal_alpha: float = 0.05,
    command_prefix: str = '',
) -> OTUTableFormat:
    """Run LEfSe and return the LEfSe result table.

    Use ``command_prefix`` to run LEfSe in a Python 2.7 environment, e.g.:
    ``conda run -n lefse-py27``.
    """
    prefix = _resolve_prefix(command_prefix)

    with tempfile.TemporaryDirectory() as tmpdir:
        formatted = os.path.join(tmpdir, 'lefse_input.in')
        results = os.path.join(tmpdir, 'lefse_results.res')

        format_args = [
            str(otu_table),
            formatted,
            '-c',
            str(class_id),
            '-o',
            str(normalization),
        ]

        if subclass_id is not None:
            format_args.extend(['-s', str(subclass_id)])
        if subject_id is not None:
            format_args.extend(['-u', str(subject_id)])

        _run_command(_lefse_cmd(prefix, 'lefse_format_input.py', format_args))

        run_args = [
            formatted,
            results,
            '-a',
            str(wilcoxon_alpha),
            '-w',
            str(kruskal_alpha),
            '-l',
            str(lda_threshold),
        ]
        _run_command(_lefse_cmd(prefix, 'lefse_run.py', run_args))

        output = OTUTableFormat()
        shutil.copyfile(results, str(output))

    return output


def visualize(
    otu_table: OTUTableFormat,
    output_dir: str,
    class_id: int,
    subclass_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    normalization: int = 1000000,
    lda_threshold: float = 2.0,
    wilcoxon_alpha: float = 0.05,
    kruskal_alpha: float = 0.05,
    command_prefix: str = '',
) -> None:
    """Run LEfSe and write visualization artifacts to ``output_dir``."""
    prefix = _resolve_prefix(command_prefix)
    os.makedirs(output_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        formatted = os.path.join(tmpdir, 'lefse_input.in')
        results = os.path.join(tmpdir, 'lefse_results.res')
        plot_res = os.path.join(output_dir, 'lefse_lda.png')
        plot_cladogram = os.path.join(output_dir, 'lefse_cladogram.png')

        format_args = [
            str(otu_table),
            formatted,
            '-c',
            str(class_id),
            '-o',
            str(normalization),
        ]
        if subclass_id is not None:
            format_args.extend(['-s', str(subclass_id)])
        if subject_id is not None:
            format_args.extend(['-u', str(subject_id)])

        _run_command(_lefse_cmd(prefix, 'lefse_format_input.py', format_args))
        _run_command(_lefse_cmd(prefix, 'lefse_run.py', [
            formatted,
            results,
            '-a',
            str(wilcoxon_alpha),
            '-w',
            str(kruskal_alpha),
            '-l',
            str(lda_threshold),
        ]))
        _run_command(_lefse_cmd(prefix, 'lefse_plot_res.py', [results, plot_res]))
        _run_command(_lefse_cmd(prefix, 'lefse_plot_cladogram.py', [results, plot_cladogram]))

        shutil.copyfile(results, os.path.join(output_dir, 'lefse_results.res'))

    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(
            '<html><body>'
            '<h1>LEfSe result</h1>'
            '<p>Result table: <a href="lefse_results.res">lefse_results.res</a></p>'
            '<h2>LDA score plot</h2><img src="lefse_lda.png" style="max-width: 100%;" />'
            '<h2>Cladogram</h2><img src="lefse_cladogram.png" style="max-width: 100%;" />'
            '</body></html>'
        )
