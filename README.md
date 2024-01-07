# q2-lefse
!!!!!!Not ready yet, just a try!
QIIME2 plugin for running lefse. originally forked from wasade/q2-humann2, not an official version, some import codes edited for new version of qiime2, 2023.2 version tested worked!

![lefse](https://github.com/Science-notes/q2-lefse/assets/20882745/8e8a454b-bed2-4946-a325-3972bd45d5ae)


## Installation

Q2-lefse requires metaphlan is in the ``$PATH``.

You can install the q2-lefse plugin through miniconda:

```bash
wget https://data.qiime2.org/distro/amplicon/qiime2-amplicon-2023.9-py38-linux-conda.yml
conda env create -n q2-lefse --file qiime2-amplicon-2023.9-py38-linux-conda.yml
source activate q2-lefse
conda install -c biobakery lefse
pip install  https://github.com/Science-notes/q2-lefse/archive/master.zip
```

## Example

The q2-lefse  plugin consumes a demultiplexed artifact from QIIME and produces gene family, pathway coverage and pathway abundance BIOM tables. 

```bash
# import data
qiime tools import  --type 'SampleData[SequencesWithQuality]'   --input-path ./01.rawdata/   --input-format CasavaOneEightSingleLanePerSampleDirFmt   --output-path demux-single-end.qza
# Imported ./01.rawdata/ as CasavaOneEightSingleLanePerSampleDirFmt to demux-single-end.qza
# run humann3, before this, prepare your databse well, especially in China, some databse may not download fastly, alternative methods can be used to do this.
qiime humann3 run --i-demultiplexed-seqs demux-single-end.qza --output-dir results --p-threads=1 --o-genefamilies gene --o-pathcoverage pathc --o-pathabundance patha  --verbose
# Output files will be written to: /tmp/tmpvm4zrc7x
# Decompressing gzipped file ...
# Running metaphlan ........
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
