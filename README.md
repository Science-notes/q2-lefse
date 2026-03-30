# q2-lefse

QIIME 2 plugin for running [LEfSe](https://huttenhower.sph.harvard.edu/galaxy/) on tab-delimited OTU-like abundance tables.

## What is implemented

This plugin now provides:

- A custom `OTUTable` semantic type and format.
- A QIIME 2 method to run `lefse_format_input.py` + `lefse_run.py`.
- A QIIME 2 visualizer that additionally generates:
  - `lefse_lda.png`
  - `lefse_cladogram.png`
  - `lefse_results.res`

## Python 2.7 compatibility strategy (important)

Many LEfSe distributions still run in Python 2.7, while QIIME 2 plugin runtime is Python 3.

This plugin supports cross-environment execution through `command_prefix`:

- per command via parameter `--p-command-prefix`
- globally via environment variable `Q2_LEFSE_COMMAND_PREFIX`

Typical setup:

```bash
conda create -n lefse-py27 python=2.7 lefse -c biobakery -c bioconda
```

Then call LEfSe from QIIME 2 env using:

```bash
--p-command-prefix "conda run -n lefse-py27"
```

or export once:

```bash
export Q2_LEFSE_COMMAND_PREFIX="conda run -n lefse-py27"
```

## Installation

Example (inside a QIIME 2 environment):

```bash
pip install .
```

> LEfSe CLI scripts (`lefse_format_input.py`, `lefse_run.py`,
> `lefse_plot_res.py`, and `lefse_plot_cladogram.py`) can be provided via
> command prefix (recommended) instead of direct `$PATH`.

## Usage

### 1) Import an OTU table

Prepare a tab-delimited `otu.txt` file (LEfSe-style input table source), then:

```bash
qiime tools import \
  --type 'SampleData[OTUTable]' \
  --input-path otu.txt \
  --output-path otu-table.qza
```

### 2) Run LEfSe

```bash
qiime lefse run \
  --i-otu-table otu-table.qza \
  --p-class-id 1 \
  --p-subclass-id 2 \
  --p-subject-id 3 \
  --p-normalization 1000000 \
  --p-lda-threshold 2.0 \
  --p-wilcoxon-alpha 0.05 \
  --p-kruskal-alpha 0.05 \
  --p-command-prefix "conda run -n lefse-py27" \
  --o-lefse-results lefse-results.qza
```

### 3) Generate visualization

```bash
qiime lefse visualize \
  --i-otu-table otu-table.qza \
  --p-class-id 1 \
  --p-subclass-id 2 \
  --p-subject-id 3 \
  --p-command-prefix "conda run -n lefse-py27" \
  --o-visualization lefse-results.qzv
```

Then inspect via:

```bash
qiime tools view lefse-results.qzv
```

## Troubleshooting

### 1) `Command not found: lefse_*`
Usually means your Python 2.7 LEfSe env is not being used.

- pass `--p-command-prefix "conda run -n lefse-py27"`
- or export `Q2_LEFSE_COMMAND_PREFIX` before running QIIME2

### 2) `CalledProcessError` with LEfSe stderr
Run the exact failed command manually (printed in the error) to verify:

- input table format
- class/subclass/subject column indexes
- LEfSe env package integrity

### 3) `conda run` is slow on clusters
Use a lightweight prefix such as `micromamba run -n lefse-py27` if available.



## Minimal sample data + one-command verification

This repository includes:

- minimal sample table: `examples/minimal_otu.txt`
- one-command verifier: `scripts/verify_minimal_pipeline.sh`

Run (inside a QIIME 2 env):

```bash
scripts/verify_minimal_pipeline.sh "conda run -n lefse-py27"
```

Or rely on env var:

```bash
export Q2_LEFSE_COMMAND_PREFIX="conda run -n lefse-py27"
scripts/verify_minimal_pipeline.sh
```

The script will:

1. import `examples/minimal_otu.txt`
2. run `qiime lefse run`
3. run `qiime lefse visualize`
4. print generated `.qza/.qzv` paths
