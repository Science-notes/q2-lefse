# q2-humann3

QIIME2 plugin for running HUMAnN3. 

## Installation

Q2-HUMAnN3 requires metaphlan2.py is in the ``$PATH``. Installation instructions can be found [here](https://bitbucket.org/biobakery/metaphlan2), and requires approximately several GBs download which is not covered by the installation steps below.

You can install the Q2-HUMAnN3 plugin through miniconda:

```bash
wget https://data.qiime2.org/distro/core/qiime2-2023.2-py38-linux-conda.yml
conda env create -n qiime2-2023.2 --file qiime2-2023.2-py38-linux-conda.yml
source activate q2-humann3
conda install numpy
conda install -c biobakery humann
pip install  https://github.com/zd200572/q2-humann3/archive/master.zip
humann_databases --download uniref uniref90_ec_filtered_diamond .
humann_databases --download chocophlan full .
```

## Example

The Q2-HUMAnN3 plugin consumes a demultiplexed artifact from QIIME and produces gene family, pathway coverage and pathway abundance BIOM tables. 

```bash
qiime2 humann3 run --i-demultiplexed-seqs seqs.qza --output-dir results --p-threads=1
```

The produced artifacts can then be fed into downstream QIIME diversity analyses:

```bash
# commands adapted from q2-dada2 plugin readme and assumes the file 
# sample-metadata.tsv is in your current working directory and is relevant for
# your data
qiime diversity beta --i-table results/pathcoverage.qza --p-metric braycurtis --o-distance-matrix bray-curtis-dm
qiime diversity pcoa --i-distance-matrix bray-curtis-dm.qza --o-pcoa bray-curtis-pc
qiime emperor plot --i-pcoa bray-curtis-pc.qza --m-sample-metadata-file sample-metadata.tsv --o-visualization bray-curtis-emperor
qiime tools view bray-curtis-emperor.qzv
```
