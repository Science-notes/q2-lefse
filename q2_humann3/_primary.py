import subprocess
import tempfile
import os

import biom
from q2_types.feature_table import FeatureTable, Frequency
from q2_types.per_sample_sequences import \
        SingleLanePerSampleSingleEndFastqDirFmt, FastqGzFormat


def _single_sample(sample: str, threads: int, output: str) -> None:
    """Run a single sample through humann2"""
    cmd = ["humann", "-i", "%s" % sample, "-o", "%s" % output,
           "--threads", "%d" % threads,
           "--output-format", "biom", "--remove-column-description-output"]
    subprocess.run(cmd, check=True)


def _join_tables(table: str, output: str, name: str) -> None:
    """Merge multiple sample output into single tables"""
    tmp_output = output + '-actual'
    cmd = ["humann_join_tables", "-i", table, "-o", tmp_output,
           "--file_name", "%s" % name]
    subprocess.run(cmd, check=True)

    # doing convert manually as we need to filter out the leading comment as
    # humann2_renorm_table cannot handle comment lines
    for_convert = biom.load_table(tmp_output)
    lines = for_convert.to_tsv().splitlines()
    lines = lines[1:]  # drop leading comment
    with open(output, 'w') as fp:
        fp.write('\n'.join(lines))
        fp.write('\n')


def _renorm(table: str, method: str, output: str) -> None:
    """Renormalize a table"""
    cmd = ["humann_renorm_table", "-i", "%s" % table, "-o", "%s" % output,
           "-u", "%s" % method]
    subprocess.run(cmd, check=True)


def run(demultiplexed_seqs: SingleLanePerSampleSingleEndFastqDirFmt,
        threads: int=1) -> (biom.Table, biom.Table, biom.Table):
    """Run samples through humann2

    Parameters
    ----------
    samples : SingleLanePerSampleSingleEndFastqDirFmt
        Samples to process
    threads : int
        The number of threads that humann3 should use

    Notes
    -----
    This command consumes per-sample FASTQs, and takes those data through
    "humann3", then through "humann_join_tables" and finalizes with
    "humann_renorm_table".

    Returns
    -------
    biom.Table
        A gene families table normalized using "cpm"
    biom.Table
        A pathway coverage table normalized by relative abundance
    biom.Table
        A pathway abundance table normalized by relative abundance
    """
    import sys
    from distutils.spawn import find_executable
    if find_executable('metaphlan') is None:
        sys.stderr.write(("Cannot find metaphlan in $PATH. Please install "
                          "metaphlan3 prior to installing the q2-humann3 "
                          "plugin as it is a required dependency. Details can "
                          "be found here: "
                          "https://github.com/biobakery/MetaPhlAn.\n"))
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmp:
        iter_view = demultiplexed_seqs.sequences.iter_views(FastqGzFormat)
        for path, view in iter_view:
            _single_sample(str(view), threads, tmp)

        final_tables = {}
        for (name, method) in [('genefamilies', 'cpm'),
                               ('pathcoverage', 'relab'),
                               ('pathabundance', 'relab')]:

            joined_path = os.path.join(tmp, "%s.biom" % name)
            result_path = os.path.join(tmp, "%s.%s.biom" % (name, method))

            _join_tables(tmp, joined_path, name)
            _renorm(joined_path, method, result_path)

            final_tables[name] = biom.load_table(result_path)

    return (final_tables['genefamilies'],
            final_tables['pathcoverage'],
            final_tables['pathabundance'])
