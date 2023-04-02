# q2-humann3

QIIME2 plugin for running HUMAnN3. forked from wasade/q2-humann2, not an official version, just changing from version 2 to version 3, some import codes edited for new version of qiime2, 2023.2 version tested worked!

![](https://user-images.githubusercontent.com/20882745/229346119-691da579-ecf6-46e9-836f-aec5007de0da.png)

## Installation

Q2-HUMAnN3 requires metaphlan is in the ``$PATH``.

You can install the Q2-HUMAnN3 plugin through miniconda:

```bash
wget https://data.qiime2.org/distro/core/qiime2-2023.2-py38-linux-conda.yml
conda env create -n q2-humann3 --file qiime2-2023.2-py38-linux-conda.yml
source activate q2-humann3
conda install -c biobakery humann
pip install  https://github.com/zd200572/q2-humann3/archive/master.zip
humann_databases --download uniref uniref90_ec_filtered_diamond .
humann_databases --download chocophlan full .
```

## Example

The Q2-HUMAnN3 plugin consumes a demultiplexed artifact from QIIME and produces gene family, pathway coverage and pathway abundance BIOM tables. 

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
